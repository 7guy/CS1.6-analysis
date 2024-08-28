/*
AMXX Kill Distance

Author: Nightscream
Help: Kleenex
Version: 0.3
===============================================
Description:
If Someone kills an enemy/teammate
it will give a hud message to see from
how far you killed him in meters

made on request
http://www.amxmodx.org/forums/viewtopic.php?t=15208
===============================================
Cvars:
distance_meter		0 = Feet
			1 = Meter
			
ditance_all		0 = shows text only to killer
			1= shows text to everyone
===============================================
Tested on:
Listen server | condition-zero | Windows XP Home | amxx 1.55
===============================================
Changelog:
0.1 - Release for amxx
0.2 - Added Distance in Feet
0.3 - Added distance_all cvar so text can be showed to everyone/killer
===============================================
suggestions are always welcome
*/

#include <amxmodx>
#include <amxmisc>

#define PLUGINNAME	"Kill Distance"
#define VERSION		"0.3"
#define AUTHOR		"Nightscream"

new Float:modMeter = 32.00
new Float:modFeet = 35.00

public plugin_init() {
	register_plugin( PLUGINNAME, VERSION, AUTHOR )
	
	register_event( "DeathMsg",  "Event_Death",  "a" ) 
	
	register_cvar( "distance_meter", "1" )
	register_cvar( "distance_all", "1" )
}

public Event_Death(id) {
	new iVictimID = read_data(2)
    	new iWeapon, iAttackerID = get_user_attacker( iVictimID, iWeapon )

    	if( !is_user_connected( iVictimID ) ) return PLUGIN_CONTINUE

    	if( !is_user_connected( iAttackerID ) || iVictimID == iAttackerID ) return PLUGIN_CONTINUE
        
	new name[33]
	new name2[33]
	get_user_name( iAttackerID, name, 32 )
	get_user_name( iVictimID, name2, 32 )
	
	new origin1[3]
	new origin2[3]
	get_user_origin( iAttackerID, origin1 )
	get_user_origin( iVictimID, origin2 )

	new distance = get_distance(origin1,origin2)
	if ( get_cvar_num( "distance_meter" ) == 0 ) {
		if ( get_cvar_num( "distance_all" ) == 1 ) {
			set_hudmessage( 0, 100, 0, 0.06, 0.8, 0, 6.0, 12.0, 0.5, 0.5, 162 );
			show_hudmessage( id, "%s have killed %s^nfrom a distance of %d feet",name, name2,floatround( distance/modFeet ) )
		}
		if ( get_cvar_num( "distance_all" ) == 0 ) {
			set_hudmessage( 0, 100, 0, 0.06, 0.8, 0, 6.0, 12.0, 0.5, 0.5, 162 );
			show_hudmessage( iAttackerID, "You have killed %s^nfrom a distance of %d feet", name2,floatround( distance/modFeet ) )
		}
	}
	if ( get_cvar_num("distance_meter") == 1 ) {
		if ( get_cvar_num( "distance_all" ) == 1 ) {
			set_hudmessage(0, 100, 0, 0.06, 0.8, 0, 6.0, 12.0, 0.5, 0.5, 162);
			show_hudmessage( id, "%s have killed %s^nfrom a distance of %d meter",name, name2,floatround( distance/modMeter ) )
		}
		if ( get_cvar_num( "distance_all" ) == 0 ) {
			set_hudmessage(0, 100, 0, 0.06, 0.8, 0, 6.0, 12.0, 0.5, 0.5, 162);
			show_hudmessage( iAttackerID, "You have killed %s^nfrom a distance of %d meter", name2,floatround( distance/modMeter ) )
		}
	}
	
	return PLUGIN_CONTINUE
}