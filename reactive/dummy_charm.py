import time

from charms import apt
from charms import reactive
from charmhelpers.core import hookenv
# from charms.reactive import when, when_not, hookenv.set_flag, clear_flag
# from charmhelpers.core.hookenv import hookenv.log, hookenv.status_set,
# application_version_set, config, relations_of_type


@reactive.when_not('dummy-charm.installed')
def install_dummy_charm():
    hookenv.status_set('maintenance', 'Installing important packages')
    apt.queue_install(['cowsay'])
    hookenv.status_set('waiting', 'Important packages installed. Waiting for activation.')
    reactive.set_flag('dummy-charm.installed')


@reactive.when('config.changed.active')
def change_activity_state():
    config = hookenv.config()
    active = config.get("active")
    hookenv.log("'active' changed in config: %s" % active)
    if active:
        hookenv.log("Activating charm from config change")
        reactive.set_flag('dummy-charm.active')
    else:
        hookenv.log("Deactivating charm from config change")
        reactive.clear_flag('dummy-charm.active')


@reactive.when('dummy-charm.active')
def do_activity():
    config = hookenv.config()
    active_period = int(config.get("active-period"))

    hookenv.status_set('maintenance', 'Doing important things for %d seconds', active_period)
    hookenv.log("Charm is actively doing something for %d seconds" % active_period)
    time.sleep(active_period)
    hookenv.log("Charm finished doing something for %d seconds" % active_period)
    reactive.clear_flag('dummy-charm.active')
    hookenv.status_set('waiting', 'Waiting for reactivation')


@reactive.when_not('dummy-charm.active')
def sleep_between_activities():
    config = hookenv.config()
    sleep_period = int(config.get("sleep-period"))
    hookenv.log("Charm will now sleep %d seconds" % sleep_period)
    hookenv.status_set('maintenance', 'Sleeping %d seconds' % sleep_period)
    time.sleep(sleep_period)
    hookenv.log("Charm finished sleeping %d between activities" % sleep_period)
    hookenv.log("Re-activating charm")
    reactive.set_flag('dummy-charm.active')


@reactive.when_not('dummy-charm.active')
def deactivate_charm():
    hookenv.log("Deactivating charm")
    reactive.clear_flag('dummy-charm.active')
