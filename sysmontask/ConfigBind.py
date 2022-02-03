def cb_network_in_bits_changed(settings,key,app):
    print("cb_network_in_bits")
    app.config.network_unit_in_bits=settings.get_boolean(key)

def cb_proc_update_interval_changed(settings,key,app):
    if key=="proc-update-interval":
        app.config.proc_interval_changed=settings.get_int(key)
        # if app.timeout:
        #     proctable_freeze(app)
        #     proctable_thaw(app)

