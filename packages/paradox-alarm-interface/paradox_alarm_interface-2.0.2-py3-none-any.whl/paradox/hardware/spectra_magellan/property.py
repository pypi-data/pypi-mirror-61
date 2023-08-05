from paradox.event import EventLevel

property_map = {
    "ac_failure_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'power'],
        message={"True": "AC Power failure",
                 "False": "AC Power restored"}),
    "ac_loss_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'power'],
        message={"True": "{Type} {label} AC Power lost",
                 "False": "{Type} {label} AC Power is OK"}),
    "alarm": dict(
        level=EventLevel.CRITICAL, tags=['alarm'],
        message={"True": "{Type} {label} in alarm",
                 "False": "{Type} {label} not in alarm"}),
    "alarms_in_memory": dict(
        level=EventLevel.INFO, tags=['alarm'],
        message={"True": "{Type} {label} has alarms in memory",
                 "False": "{Type} {label} alarms memory empty"}),
    "arm": dict(
        level=EventLevel.INFO, tags=['arm'],
        message={"True": "{Type} {label} is armed",
                 "False": "{Type} {label} is disarmed"}),
    "arm_force": dict(
        level=EventLevel.INFO, tags=['arm'],
        message={"True": "{Type} {label} forced arm",
                 "False": "{Type} {label} arm not forced"}),
    "arm_sleep": dict(
        level=EventLevel.INFO, tags=['arm'],
        message={"True": "{Type} {label} sleep arm is active",
                 "False": "{Type} {label} sleep arm is inactive"}),
    "arm_stay": dict(
        level=EventLevel.INFO, tags=['arm'],
        message={"True": "{Type} {label} stay arm active",
                 "False": "{Type} {label} stay arm inactive"}),
    "arm_with_remote": dict(
        level=EventLevel.INFO, tags=['arm'],
        message={"True": "{Type} {label} is armed with remote",
                 "False": "{Type} {label} is not armed with remote"}),
    "audible_alarm": dict(
        level=EventLevel.CRITICAL, tags=['alarm'],
        message={"True": "{Type} {label} alarm is audible",
                 "False": "{Type} {label} alarm is silent"}),
    "auto_arming_engaged": dict(
        level=EventLevel.CRITICAL, tags=['arm'],
        message={"True": "{Type} {label} auto arming engaged",
                 "False": "{Type} {label} auto arming is not engaged"}),
    "auxiliary_output_overload_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'output'],
        message={"True": "Auxiliary output overloaded",
                 "False": "Auxiliary output load is adequate"}),
    'battery': dict(
        level=EventLevel.DEBUG, tags=['voltage', 'battery'],
        message="Battery voltage is {value}V"),
    "battery_failure_trouble": dict(
        level=EventLevel.CRITICAL, tags=['battery', 'trouble'],
        message={"True": "{Type} {label} battery is low",
                 "False": "{Type} {label} battery is OK"}),
    "bell_activated": dict(
        level=EventLevel.CRITICAL, tags=['bell', 'alarm'],
        message={"True": "{Type} {label} bell is active",
                 "False": "{Type} {label} bell is inactive"}),
    "bell_delay_finished": dict(
        level=EventLevel.CRITICAL, tags=['bell', 'alarm'],
        message={"True": "{Type} {label} bell delay is inactive",
                 "False": "{Type} {label} bell delay is active"}),
    "bell_output_disconnected_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'bell'],
        message={"True": "Bell output disconnected",
                 "False": "Bell output connected"}),
    "bell_output_overload_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'bell'],
        message={"True": "Bell output overloaded",
                 "False": "Bell output load is adequate"}),
    "bell_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'bell'],
        message={"True": "Bell trouble",
                 "False": "Bell restored"}),
    "bypassed": dict(
        level=EventLevel.INFO,
        message={"True": "{Type} {label} bypassed",
                 "False": "{Type} {label} not bypassed"}),
    "central_1_reporting_ftc_indicator_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'central'],
        message={"True": "Central 1 reporting trouble",
                 "False": "Central 1 reporting OK"}),
    "central_2_reporting_ftc_indicator_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'central'],
        message={"True": "Central 2 reporting trouble",
                 "False": "Central 2 reporting OK"}),
    "communication_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'communication'],
        message={"True": "Communication trouble",
                 "False": "Communication restored"}),
    "computer_fail_to_communicate_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'communication'],
        message={"True": "PC communication failed",
                 "False": "PC communication OK"}),
    'dc': dict(
        level=EventLevel.DEBUG, tags=['voltage', 'power'],
        message="DC voltage is {value}V"),
    "entry_delay": dict(
        level=EventLevel.INFO, tags=['alarm'],
        message={"True": "{Type} {label} in entry delay",
                 "False": "{Type} {label} not in entry delay"}),
    "entry_delay_finished": dict(
        level=EventLevel.DEBUG, tags=['alarm'],
        message={"True": "{Type} {label} entry delay is finished",
                 "False": "{Type} {label} entry delay is not finished"}),
    "exit_delay": dict(
        level=EventLevel.INFO, tags=['arm'],
        message={"True": "{Type} {label} in exit delay",
                 "False": "{Type} {label} not in exit delay"}),
    "exit_delay_finished": dict(
        level=EventLevel.DEBUG, tags=['arm'],
        message={"True": "{Type} {label} exit delay is finished",
                 "False": "{Type} {label} exit delay is not finished"}),
    "fire_delay": dict(
        level=EventLevel.INFO, tags=['alarm', 'fire'],
        message={"True": "{Type} {label} is in fire delay",
                 "False": "{Type} {label} is in fire delay"}),
    "fire": dict(
        level=EventLevel.CRITICAL, tags=['alarm', 'fire'],
        message={"True": "{Type} {label} fire",
                 "False": "{Type} {label} has no fire"}),
    "fire_loop_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble'],
        message={"True": "Fire loop",
                 "False": "Fire loop recovered"}),
    "in_remote_delay": dict(
        level=EventLevel.DEBUG,
        message={"True": "{Type} {label} in remote delay",
                 "False": "{Type} {label} not in remote delay"}),
    "intellizone_delay": dict(
        level=EventLevel.DEBUG,
        message={"True": "{Type} {label} in intellizone delay",
                 "False": "{Type} {label} not in intellizone delay"}),
    "intellizone_delay_finished": dict(
        level=EventLevel.DEBUG,
        message={"True": "{Type} {label} intellizone delay finished",
                 "False": "{Type} {label} intellizone delay is active"}),
    "in_tx_delay": dict(
        level=EventLevel.DEBUG,
        message={"True": "{Type} {label} in TX delay",
                 "False": "{Type} {label} not in TX delay"}),
    "keypad_battery_failure_trouble": dict(
        level=EventLevel.CRITICAL, tags=['battery', 'trouble'],
        message={"True": "Keypad {l} battery is low",
                 "False": "Keypad {label} battery is OK"}),
    "low_battery_trouble": dict(
        level=EventLevel.CRITICAL, tags=['battery', 'trouble'],
        message={"True": "{Type} {label} Battery is low",
                 "False": "{Type} {label} Battery level is adequate"}),
    "module_supervision_trouble": dict(
        level=EventLevel.CRITICAL, tags=['supervision', 'trouble'],
        message={"True": "Module supervision trouble",
                 "False": "Module supervision OK"}),
    "module_tamper_trouble": dict(
        level=EventLevel.CRITICAL, tags=['tamper', 'trouble'],
        message={"True": "Module tampered",
                 "False": "Module tamper cleared"}),
    "no_delay": dict(
        level=EventLevel.CRITICAL,
        message={"True": "{Type} {label} has no delay",
                 "False": "{Type} {label} has a delay active"}),
    "open": dict(
        level=EventLevel.DEBUG,
        message={"True": "Zone {label} open",
                 "False": "Zone {label} closed"}),
    "pager_fail_to_communicate_trouble": dict(
        level=EventLevel.CRITICAL, tags=['pager', 'communication', 'trouble'],
        message={"True": "Pager communication failed",
                 "False": "Pager communication OK"}),
    "paramedic_alarm": dict(
        level=EventLevel.CRITICAL, tags=['alarm', 'medic'],
        message={"True": "{Type} {label} paramedic alarm active",
                 "False": "{Type} {label} paramedic alarm is inactive"}),
    "power_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'power'],
        message={"True": "Power trouble",
                 "False": "Power restored"}),
    "pulse_fire_alarm": dict(
        level=EventLevel.CRITICAL, tags=['fire', 'alarm'],
        message={"True": "{Type} {label} fire alarm pulse is active",
                 "False": "{Type} {label} fire alarm pulse is inactive"}),
    "ready_status": dict(
        level=EventLevel.DEBUG,
        message={"True": "{Type} {label} ready",
                 "False": "{Type} {label} not ready"}),
    "recent_closing_delay": dict(
        level=EventLevel.DEBUG,
        message={"True": "{Type} {label} recent closing delay",
                 "False": "{Type} {label} no recent closing delay"}),
    "rf_interference_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'rf', 'interference'],
        message={"True": "RF Interference trouble",
                 "False": "RF Interference cleared"}),
    "rf_low_battery_trouble": dict(
        level=EventLevel.CRITICAL, tags=['trouble', 'rf', 'battery'],
        message={"True": "{Type} {label} RF battery low",
                 "False": "{Type} {label} RF battery OK"}),
    'noise_floor': dict(
        level=EventLevel.DEBUG, tags=['rf', 'interference'],
        message="RF Noise floor is {value}"),
    "rf_supervision_trouble": dict(
        level=EventLevel.CRITICAL, tags=['rf', 'supervision', 'trouble'],
        message={"True": "{Type} {label} has supervision trouble",
                 "False": "{Type} {label} has no supervision trouble"}),
    "shutdown": dict(
        level=EventLevel.INFO,
        message={"True": "{Type} {label} is shutdown",
                 "False": "{Type} {label} is active"}),
    "signal_strength": dict(
        level=EventLevel.DEBUG, tags=['rf'],
        message="{Type} {label} signal strength {value}"),
    "silent_alarm": dict(
        level=EventLevel.CRITICAL, tags=['alarm'],
        message={"True": "{Type} {label} silent alarm is active",
                 "False": "{Type} {label} silent alarm is inactive"}),
    "squawk": dict(
        level=EventLevel.DEBUG,
        message={"True": "{Type} {label} Squawk On",
                 "False": "{Type} {label} Squawk Off"}),
    "stayd_mode_active": dict(
        level=EventLevel.DEBUG,
        message={"True": "{Type} {label} StayD mode is active",
                 "False": "{Type} {label} StayD mode is inactive"}),
    "strobe_alarm": dict(
        level=EventLevel.CRITICAL, tags=['alarm'],
        message={"True": "{Type} {label} Alarm Strobe is active",
                 "False": "{Type} {label} Alarm Strobe is inactive"}),
    "supervision_failure_trouble": dict(
        level=EventLevel.CRITICAL, tags=['supervision', 'trouble'],
        message={"True": "{Type} {label} supervision lost",
                 "False": "{Type} {label} supervision is OK"}),
    "supervision_trouble": dict(
        level=EventLevel.CRITICAL, tags=['supervision', 'trouble'],
        message={"True": "{Type} {label} supervision trouble",
                 "False": "{Type} {label} supervision OK"}),
    "tamper": dict(
        level=EventLevel.CRITICAL, tags=['tamper', 'trouble'],
        message={"True": "{Type} {label} tampered",
                 "False": "{Type} {label} tamper cleared"}),
    "telephone_line": dict(
        level=EventLevel.CRITICAL, tags=['telephone', 'communication', 'trouble'],
        message={"True": "Telephone line trouble",
                 "False": "Telephone line OK"}),
    'timer_loss_trouble': dict(
        level=EventLevel.CRITICAL, tags=['timer', 'trouble'],
        message={"True": "Timer lost trouble",
                 "False": "Timer recovered"}),
    "transmission_delay_finished": dict(
        level=EventLevel.DEBUG,
        message={"True": "{Type} {label} Transmission delay finished",
                 "False": "{Type} {label} Transmission delay is active"}),
    'trouble': dict(
        level=EventLevel.CRITICAL, tags=['trouble'],
        message={"True": "{Type} {label} has trouble",
                 "False": "No trouble for {Type} {label}"}),
    'vdc': dict(
        level=EventLevel.DEBUG, tags=['voltage', 'power'],
        message="VDC voltage is {value}V"),
    "voice_fail_to_communicate_trouble": dict(
        level=EventLevel.CRITICAL, tags=['voice', 'communication', 'trouble'],
        message={"True": "Voice module communication failed",
                 "False": "Voice module communication OK"}),
    "wait_window": dict(
        level=EventLevel.DEBUG,
        message={"True": "{Type} {label} wait window is active",
                 "False": "{Type} {label} wait window is inactive"}),
    "was_bypassed": dict(
        level=EventLevel.INFO,
        message={"True": "{Type} {label} was bypassed",
                 "False": "{Type} {label} was not bypassed"}),
    "was_in_alarm": dict(
        level=EventLevel.INFO, tags=['alarm'],
        message={"True": "{Type} {label} was in alarm",
                 "False": "{Type} {label} was not in alarm"}),
    "wireless_keypad_ac_trouble": dict(
        level=EventLevel.CRITICAL, tags=['ac', 'power', 'trouble'],
        message={"True": "Wireless Keypad AC power with trouble",
                 "False": "Wireless Keypad AC power OK"}),
    "wireless_keypad_battery_trouble": dict(
        level=EventLevel.CRITICAL, tags=['battery', 'trouble'],
        message={"True": "Wireless Keypad battery with trouble",
                 "False": "Wireless Keypad battery OK"}),
    "wireless_repeater_ac_loss_trouble": dict(
        level=EventLevel.CRITICAL, tags=['ac', 'power', 'trouble'],
        message={"True": "Wireless Repeater with AC power failure",
                 "False": "Wireless Repeater AC power is OK"}),
    "wireless_repeater_battery_trouble": dict(
        level=EventLevel.CRITICAL, tags=['battery', 'trouble'],
        message={"True": "Wireless Repeater battery with trouble",
                 "False": "Wireless Repeater battery OK"}),
    "zone_bypassed": dict(
        level=EventLevel.INFO,
        message={"True": "{Type} {label} is bypassed",
                 "False": "{Type} {label} is not bypassed"}),
    "zone_supervision_trouble": dict(
        level=EventLevel.CRITICAL, tags=['supervision', 'trouble'],
        message={"True": "Zone with supervision trouble",
                 "False": "Zone supervision is OK"}),
    "zone_tamper_trouble": dict(
        level=EventLevel.CRITICAL, tags=['tamper', 'trouble'],
        message={"True": "Zone tampered",
                 "False": "No Zone is tampered"}),
    "time": dict(
        level=EventLevel.DEBUG, tags=['system', 'time'],
        message="Panel time is {value}"),

    # ---------------------
    # Synthetic properties
    # ---------------------
    "current_state": dict(
        level=EventLevel.INFO,
        tags=[],
        message={
            "triggered": "{Type} {label} triggered alarm",
            "pending": "{Type} {label} arming pending",
            "armed_home": "{Type} {label} armed stay",
            "armed_away": "{Type} {label} armed away",
            "disarmed": "{Type} {label} disarmed"
        }
    )
}
