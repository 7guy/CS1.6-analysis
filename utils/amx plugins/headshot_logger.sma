/*
AMXX Headshot Logger

Author: You
Version: 1.0
===============================================
Description:
Logs whether a kill was a headshot to the server console.

Tested on:
Listen server | condition-zero | amxx 1.55
Dedicated server | gearbox | amxx 1.10
===============================================
*/

#include <amxmodx>
#include <amxmisc>

#define PLUGINNAME  "Headshot Logger"
#define VERSION     "1.0"
#define AUTHOR      "Your Name"

#if !defined MAX_PLAYERS
#define MAX_PLAYERS 32
#endif

public plugin_init()
{
    register_plugin( PLUGINNAME, VERSION, AUTHOR )
    register_event("DeathMsg", "Event_Death", "a")
}

public Event_Death()
{
    new iVictimID = read_data(2)
    new iAttackerID = read_data(1)
    new headshot = read_data(3)  // The third data slot in "DeathMsg" is the headshot flag (1 if headshot, 0 if not)
    
    if (!is_user_connected(iVictimID) || !is_user_connected(iAttackerID))
        return PLUGIN_HANDLED_MAIN

    // Get player names
    new victimName[MAX_PLAYERS+1]
    new attackerName[MAX_PLAYERS+1]
    get_user_name(iVictimID, victimName, charsmax(victimName))
    get_user_name(iAttackerID, attackerName, charsmax(attackerName))

    // Check if it's a headshot
    if (headshot == 1)
    {
        log_message("%s killed %s with a headshot!", attackerName, victimName)
    }
    else
    {
        log_message("%s killed %s without a headshot.", attackerName, victimName)
    }

    return PLUGIN_CONTINUE
}
