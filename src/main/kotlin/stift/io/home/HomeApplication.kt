package stift.io.home

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.context.properties.ConfigurationPropertiesScan
import org.springframework.boot.runApplication

@ConfigurationPropertiesScan
@SpringBootApplication
class HomeApplication

fun main(args: Array<String>) {
	runApplication<HomeApplication>(*args)
}
