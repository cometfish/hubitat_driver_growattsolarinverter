metadata {
    definition(name: "Growatt Solar Inverter", namespace: "community", author: "cometfish", importUrl: "https://raw.githubusercontent.com/cometfish/hubitat_driver_growattsolarinverter/master/growatt.groovy") {
        capability "PowerMeter"
        capability "EnergyMeter"
        capability "Polling"
        capability "TemperatureMeasurement"
        capability "VoltageMeasurement"

        attribute "power", "number"
        attribute "energy", "number"
        attribute "energy_total", "number"
        attribute "hours_total", "number"
        attribute "temperature", "number"
        attribute "input_power", "number"
        attribute "output_power", "number"
        attribute "input_voltage", "number"
        attribute "input_voltage2", "number"
        attribute "grid_voltage", "number"
        attribute "current", "number"
        attribute "frequency", "number"
        attribute "status", "text"
        attribute "lastupdate", "date"
        
        attribute "tile", "text"

        command "poll"
    }
}

preferences {
    section("URIs") {
        input "scriptURL", "text", title: "Script Address", required: true
		
        input name: "logEnable", type: "bool", title: "Enable debug logging", defaultValue: true
    }
}

def updated() {
    log.info "updated..."
    log.warn "debug logging is: ${logEnable == true}"
    
	unschedule()
    
    Random rand = new Random(now())
    def randomSeconds = rand.nextInt(60)
    def sched = "${randomSeconds} 0/5 * * * ?"
    schedule("${sched}", "poll")
}

def poll() {


 
    if (logEnable) log.debug settings.scriptURL

    httpGet(["uri":settings.scriptURL]) { resp ->
        if (resp.success) {
            if (resp.data.error!= null) {
                if (resp.data.error != 'no response')
                    log.error resp.data.error
            } else {
                sendEvent(name: "lastupdate", value: new Date(), isStateChange: true)

                sendEvent(name: "temperature", value: resp.data.temperature, unit: "°C", isStateChange: true)
                sendEvent(name: "power", value: resp.data.output_power, unit: "W", isStateChange: true)
                sendEvent(name: "energy", value: resp.data.energy_today, unit: "kWh", isStateChange: true)

                sendEvent(name: "output_power", value: resp.data.output_power, unit: "W", isStateChange: true)
                sendEvent(name: "energy_total", value: resp.data.energy_total, unit: "kWh", isStateChange: true)
                sendEvent(name: "input_power", value: resp.data.input_power, unit: "W", isStateChange: true)
                sendEvent(name: "hours_total", value: resp.data.hours_total, unit: "hrs", isStateChange: true)
                sendEvent(name: "input_voltage", value: resp.data.input_voltage, unit: "V", isStateChange: true)
                sendEvent(name: "input_voltage2", value: resp.data.input_voltage2, unit: "V", isStateChange: true)
                sendEvent(name: "grid_voltage", value: resp.data.grid_voltage, unit: "V", isStateChange: true)
                sendEvent(name: "current", value: resp.data.current, unit: "A", isStateChange: true)
                sendEvent(name: "frequency", value: resp.data.frequency, unit: "Hz", isStateChange: true)
                sendEvent(name: "status", value: resp.data.status_desc, unit: "", isStateChange: true)
                
                def colour = "#f00"
                if (resp.data.output_power>=100)
                   colour = "#0f0" 
                else if (resp.data.output_power>=50)
                    colour = "#0ff"
                def tilehtml = "<br><span style='font-size:30px;color:" +colour+"'>" +resp.data.output_power+"W</span><br><span style='font-size:12px;color:#aaa'>Total:" +resp.data.energy_today+"kWh</span>"

                sendEvent(name: "tile", value: tilehtml, isStateChange: true)

  
           }
        } else {
            log.error "Error: ${resp}"
        }
    }			
}


     