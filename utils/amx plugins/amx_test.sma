#include <amxmodx>
#include <amxmisc>

#define PLUGIN_NAME "Simple Test Plugin"
#define PLUGIN_VERSION "1.0"
#define PLUGIN_AUTHOR "YourName"

// Log a message when the plugin is loaded
public plugin_init()
{
    log_to_file("plugin.log", "Simple Test Plugin loaded\n"); // Log to AMX Mod X log
    log_amx("Simple Test Plugin loaded"); // Log to server console
    register_plugin(PLUGIN_NAME, PLUGIN_VERSION, PLUGIN_AUTHOR);
    register_event("DeathMsg", "onKill", "a");
}

// Event handler for kills
public onKill()
{
    log_to_file("plugin.log", "Kill event detected\n"); // Log to AMX Mod X log
    log_amx("Kill event detected"); // Log to server console
    client_print(0, print_center, "Hi team"); // Display message to all players
    return PLUGIN_CONTINUE;
}
