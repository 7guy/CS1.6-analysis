#include <amxmodx>
#include <amxmisc>

#define PLUGIN "Hi Team on Kill"
#define VERSION "1.0"
#define AUTHOR "YourName"

public plugin_init()
{
    // Register the plugin
    register_plugin(PLUGIN, VERSION, AUTHOR);

    // Register the DeathMsg event to trigger on kill
    register_event("DeathMsg", "onKill", "a");
}

// Function that is triggered when a kill happens
public onKill()
{
    // Display "Hi team" on the screen to all players
    client_print(0, print_center, "Hi team");
    
    return PLUGIN_CONTINUE;
}
