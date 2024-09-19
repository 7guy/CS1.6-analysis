/*
AMXX Kill Distance

Author: Nightscream
Help: Kleenex, SPiNX
Version: 0.5
===============================================
Description:
If someone kills an enemy/teammate,
it will log a message to see from
how far you killed them in meters.

URL:
https://forums.alliedmods.net/showpost.php?p=2663653&postcount=28
===============================================
Cvars:
distance_meter 0 = Feet
            1 = Meter

distance_all   0 = shows text only to killer
            1 = shows text to everyone
===============================================
Tested on:
Listen server | condition-zero | Windows XP Home | amxx 1.55
Dedicated server | gearbox | Debian 4.19.132-1 (2020-07-24) x86_64 | amxx 1.10
===============================================
Changelog:
0.1 - Release for amxx
0.2 - Added Distance in Feet
0.3 - Added distance_all cvar so text can be showed to everyone/killer
0.3 - Ported to HL at some point. Shared  on Allied Modders 08-18-2019.
0.4 - Added distance_showtime cvar for HUD distance time. Optimized.
0.5 - Resolved as admin sometimes see floods of Cbuf_AddTextToBuffer: overflow with occasional CbufAddTextToBuffer: overflow.
      Possible inexplicable client buffer overflows on Windows. We never see the condump.
      Reason was HUD was sending to id when 0 is global whereas id should be a single client.
      SEPT 2020.
===============================================
Suggestions are always welcome
*/

#include <amxmodx>
#include <amxmisc>

#define PLUGINNAME  "Kill Distance"
#define VERSION     "0.5"
#define AUTHOR      "Nightscream|SPiNX"

#if !defined MAX_PLAYERS
#define MAX_PLAYERS 32
#endif

new Float:modMeter = 32.00
new Float:modFeet  = 35.00
new iAll, iMetr, iPost;

public plugin_init()
{
    register_plugin( PLUGINNAME, VERSION, AUTHOR )
    register_event( "DeathMsg",  "Event_Death",  "a" )

    iAll   = register_cvar( "distance_all", "1" )
    iMetr  = register_cvar( "distance_meter", "1" )
    iPost  = register_cvar( "distance_showtime", "5" )
}

public Event_Death(id)
{
    new iVictimID = read_data(2)

    new iAttackerID, iWeapon;

    if( !is_user_connected( iVictimID ) )
        return PLUGIN_HANDLED_MAIN

    iAttackerID = get_user_attacker( iVictimID, iWeapon )

    if( !is_user_connected( iAttackerID ) || iVictimID == iAttackerID )
        return PLUGIN_HANDLED_MAIN

    new name[MAX_PLAYERS+1]
    new name2[MAX_PLAYERS+1]
    get_user_name( iAttackerID, name, charsmax(name) )
    get_user_name( iVictimID, name2, charsmax(name2) )

    new origin1[3]
    new origin2[3]
    get_user_origin( iAttackerID, origin1 )
    get_user_origin( iVictimID, origin2 )

    if (iAttackerID == 0 || iVictimID == 0) return PLUGIN_HANDLED_MAIN;

    new distance = get_distance(origin1, origin2)

    if (get_pcvar_num(iMetr) == 0)
    {
        if (get_pcvar_num(iAll) == 1)
        {
            log_message("%s have killed %s from a distance of %d feet", name, name2, floatround(distance/modFeet))
        }

        if (get_pcvar_num(iAll) == 0)
        {
            log_message("You have killed %s from a distance of %d feet", name2, floatround(distance/modFeet))
        }
    }

    if (get_pcvar_num(iMetr) == 1)
    {
        if (get_pcvar_num(iMetr) == 1)
        {
            log_message("%s have killed %s from a distance of %d meters", name, name2, floatround(distance/modMeter))
        }

        if (get_pcvar_num(iAll) == 0)
        {
            log_message("You have killed %s from a distance of %d meters", name2, floatround(distance/modMeter))
        }
    }

    return PLUGIN_CONTINUE
}
