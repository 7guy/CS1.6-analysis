/*
    Headshot Logger Plugin
    Author: YourName
    Version: 1.0
    Description: Logs headshots to the game console.
*/

#include <amxmodx>
#include <amxmisc>

public plugin_init() 
{
    // Register the plugin with AMXX
    register_plugin("Headshot Logger", "1.0", "YourName");

    // Log a test message to the server console to verify that the plugin is loaded
    server_print("Headshot Logger Plugin Loaded.");

    // Register an event to track kills (including headshots)
    register_event("DeathMsg", "log_headshot", "a");
}

public log_headshot() 
{
    // Variables to store killer and victim information
    new victim = read_data(2);  // The victim of the kill
    new attacker = read_data(1);  // The attacker who performed the kill
    new headshot = read_data(3);  // Was it a headshot?

    // Ensure that the victim and attacker are valid players and connected
    if (!is_user_connected(victim) || !is_user_connected(attacker)) {
        return PLUGIN_CONTINUE;
    }

    // Check if the kill was a headshot
    if (headshot == 1) {
        // Get the attacker and victim names
        new attacker_name[32], victim_name[32];
        get_user_name(attacker, attacker_name, charsmax(attacker_name));
        get_user_name(victim, victim_name, charsmax(victim_name));

        // Log the headshot information to the server console
        server_print("%s killed %s with a headshot.", attacker_name, victim_name);
    }

    return PLUGIN_CONTINUE;
}
