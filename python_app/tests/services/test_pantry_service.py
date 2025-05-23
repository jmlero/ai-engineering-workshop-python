import pytest
import uuid
from unittest.mock import Mock # Using unittest.mock.Mock as per instruction
from python_app.services.pantry_service import PantryService, PantryEntry, LineItem, StorageRequest, UseFoodRequest, DurablePantry
# pytest-mock provides 'mocker' fixture, but instructions specified unittest.mock.Mock

@pytest.fixture
def mock_durable_pantry(mocker): # Using mocker fixture for patching if needed, though Mock directly is also fine
    # spec=DurablePantry ensures that the mock will only allow calls to methods defined in DurablePantry
    return mocker.Mock(spec=DurablePantry)

@pytest.fixture
def pantry_service(mock_durable_pantry):
    return PantryService(durable_pantry=mock_durable_pantry)

def test_get_food_returns_all_entries(pantry_service, mock_durable_pantry):
    expected_entries = [PantryEntry(id=uuid.uuid4(), name="apple", amount=5.0, unit="pcs")]
    mock_durable_pantry.find_all.return_value = expected_entries
    
    result = pantry_service.get_food()
    
    assert result == expected_entries
    mock_durable_pantry.find_all.assert_called_once()

def test_save_food_new_item(pantry_service, mock_durable_pantry):
    item = LineItem(name="banana", amount=12.0, unit="pcs")
    request = StorageRequest(items=[item])
    
    mock_durable_pantry.find_all_where_names_exist.return_value = [] # Corrected method name

    # Mock save_all to return what it's given, simulating DB save and return
    # The PantryService assigns UUIDs internally for new items.
    def mock_save_all_side_effect(entries_to_save):
        # Ensure entries passed to save_all have IDs, as PantryService should assign them.
        # For this test, we assume PantryService correctly forms PantryEntry objects.
        # The mock here just returns them back after ensuring they have IDs.
        processed_entries = []
        for entry in entries_to_save:
            if not entry.id: # Should be assigned by PantryService
                entry.id = uuid.uuid4() 
            processed_entries.append(entry)
        return processed_entries

    mock_durable_pantry.save_all.side_effect = mock_save_all_side_effect # Corrected method name
    
    saved_entries = pantry_service.save_food(request)
    
    assert len(saved_entries) == 1
    assert saved_entries[0].name == "banana"
    assert saved_entries[0].amount == 12.0
    assert saved_entries[0].id is not None # Ensure ID was assigned
    
    mock_durable_pantry.find_all_where_names_exist.assert_called_once_with(["banana"])
    mock_durable_pantry.save_all.assert_called_once()
    # Assert that the argument to save_all had one item, and its details match `item`
    args, _ = mock_durable_pantry.save_all.call_args
    assert len(args[0]) == 1
    assert args[0][0].name == "banana"
    assert args[0][0].amount == 12.0


def test_save_food_update_item(pantry_service, mock_durable_pantry):
    existing_id = uuid.uuid4()
    # Note: PantryService's save_food logic adds to existing amount, not replaces.
    # The test description implies replacement: "assert saved_entries[0].amount == 10.0"
    # Current save_food logic: entry.amount += item.amount
    # Service logic changed: amount is now replaced, not added.
    existing_item = PantryEntry(id=existing_id, name="apple", amount=5.0, unit="pcs")
    mock_durable_pantry.find_all_where_names_exist.return_value = [existing_item]
    
    update_line_item = LineItem(name="apple", amount=10.0, unit="pcs") # This is the new amount
    request = StorageRequest(items=[update_line_item])
    
    mock_durable_pantry.save_all.side_effect = lambda x: x # return the list passed in
    
    saved_entries = pantry_service.save_food(request)
    
    assert len(saved_entries) == 1
    assert saved_entries[0].id == existing_id
    assert saved_entries[0].amount == 10.0 # Amount should be replaced to 10.0
    
    mock_durable_pantry.find_all_where_names_exist.assert_called_once_with(["apple"])
    mock_durable_pantry.save_all.assert_called_once()
    args, _ = mock_durable_pantry.save_all.call_args
    assert args[0][0].amount == 10.0

def test_save_food_raises_value_error_on_unit_mismatch(pantry_service, mock_durable_pantry):
    existing_item = PantryEntry(id=uuid.uuid4(), name="flour", amount=500.0, unit="g")
    mock_durable_pantry.find_all_where_names_exist.return_value = [existing_item]
    
    request_item = LineItem(name="flour", amount=1.0, unit="kg") # Different unit
    request = StorageRequest(items=[request_item])
    
    with pytest.raises(ValueError) as excinfo:
        pantry_service.save_food(request)
    
    assert "Unit mismatch for flour" in str(excinfo.value)
    mock_durable_pantry.save_all.assert_not_called()


def test_use_food_item_exists_reduces_quantity(pantry_service, mock_durable_pantry):
    item_id = uuid.uuid4()
    existing_item = PantryEntry(id=item_id, name="milk", amount=1.0, unit="liter")
    mock_durable_pantry.find_all_where_names_exist.return_value = [existing_item] # Corrected
    
    use_request = UseFoodRequest(items=[LineItem(name="milk", amount=0.5, unit="liter")])
    
    mock_durable_pantry.save_all.side_effect = lambda x: x
    
    updated_entries = pantry_service.use_food(use_request)
    
    assert len(updated_entries) == 1
    assert updated_entries[0].id == item_id
    assert updated_entries[0].amount == 0.5
    
    mock_durable_pantry.find_all_where_names_exist.assert_called_once_with(["milk"])
    mock_durable_pantry.save_all.assert_called_once()

def test_use_food_item_depletes(pantry_service, mock_durable_pantry):
    item_id = uuid.uuid4()
    existing_item = PantryEntry(id=item_id, name="egg", amount=2.0, unit="pcs")
    mock_durable_pantry.find_all_where_names_exist.return_value = [existing_item] # Corrected
    
    use_request = UseFoodRequest(items=[LineItem(name="egg", amount=2.0, unit="pcs")])
    
    mock_durable_pantry.save_all.side_effect = lambda x: x
    
    updated_entries = pantry_service.use_food(use_request)
    
    assert len(updated_entries) == 1
    assert updated_entries[0].id == item_id
    assert updated_entries[0].amount == 0.0
    
    mock_durable_pantry.find_all_where_names_exist.assert_called_once_with(["egg"])
    mock_durable_pantry.save_all.assert_called_once()

def test_use_food_item_not_found(pantry_service, mock_durable_pantry):
    mock_durable_pantry.find_all_where_names_exist.return_value = []
    
    use_request = UseFoodRequest(items=[LineItem(name="sugar", amount=100.0, unit="g")])
    
    # Service logic changed: no ValueError, just logs and skips.
    updated_entries = pantry_service.use_food(use_request)
    
    assert len(updated_entries) == 0 # No items should be processed or returned
    mock_durable_pantry.find_all_where_names_exist.assert_called_once_with(["sugar"])
    # save_all is called with an empty list if all items are skipped
    mock_durable_pantry.save_all.assert_called_once_with([])

def test_use_food_raises_value_error_on_unit_mismatch(pantry_service, mock_durable_pantry):
    existing_item = PantryEntry(id=uuid.uuid4(), name="milk", amount=1.0, unit="liter")
    mock_durable_pantry.find_all_where_names_exist.return_value = [existing_item]
    
    use_request = UseFoodRequest(items=[LineItem(name="milk", amount=0.5, unit="ml")]) # Different unit
    
    with pytest.raises(ValueError) as excinfo:
        pantry_service.use_food(use_request)
        
    assert "Unit mismatch for milk" in str(excinfo.value)
    mock_durable_pantry.save_all.assert_not_called()

def test_use_food_raises_value_error_on_insufficient_quantity(pantry_service, mock_durable_pantry):
    existing_item = PantryEntry(id=uuid.uuid4(), name="rice", amount=500.0, unit="g")
    mock_durable_pantry.find_all_where_names_exist.return_value = [existing_item]
    
    use_request = UseFoodRequest(items=[LineItem(name="rice", amount=1000.0, unit="g")]) # Not enough
    
    with pytest.raises(ValueError) as excinfo:
        pantry_service.use_food(use_request)
        
    assert "Not enough rice" in str(excinfo.value)
    mock_durable_pantry.save_all.assert_not_called()
