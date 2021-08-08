from emoji import EMOJI_ALIAS_UNICODE_ENGLISH as EMOJIS

BOT_USER_ID = 872984503726010398
DUELING_DISCORD_ID = 757637325583810641

###############################
###### CHANNEL IDS ############
###############################

ANNOUNCEMENTS_CHANNEL_ID = 757637869689897070
LOBBY_CHANNEL_ID = 757637677607813181
GAMEPLAY_CHANNEL_ID = 757637754413908038
GAME_SIGNUPS_CHANNEL_ID = 872950109946675270
BOT_LOG_CHANNEL_ID = 872967948409655336
GAME_LOG_CHANNEL_ID = 873388957763768431

###############################
######### ROLE IDS ############
###############################

TRIVIA_TUESDAY_ROLE_ID = 872955587489591327
CURRENT_PLAYER_ROLE_ID = 757653219257090050

GRYFFINDOR_ROLE_ID = 757638791954694173
HUFFLEPUFF_ROLE_ID = 757638513381343242
RAVENCLAW_ROLE_ID = 757638926826602688
SLYTHERIN_ROLE_ID = 757638961207443497
HOUSE_ROLES = [GRYFFINDOR_ROLE_ID, HUFFLEPUFF_ROLE_ID, RAVENCLAW_ROLE_ID, SLYTHERIN_ROLE_ID]

ELITE_ROLE_ID = 757654433470480565
XPERT_ROLE_ID = 757654287466758144
ADVANCE_ROLE_ID = 757654501845893200
CASUAL_ROLE_ID = 757654534049890415
TROLL_ROLE_ID = 757654563095445605
TIER_ROLES = [ELITE_ROLE_ID, XPERT_ROLE_ID, ADVANCE_ROLE_ID, CASUAL_ROLE_ID, TROLL_ROLE_ID]

###############################
######### EMOJI IDS ###########
###############################

GRYFFINDOR_EMOJI = "<:gryffindor:872946452664569906>"
HUFFLEPUFF_EMOJI = "<:hufflepuff:872946452161265665>"
RAVENCLAW_EMOJI = "<:ravenclaw:872946452551311360>"
SLYTHERIN_EMOJI = "<:slytherin:872946452832325722>"

SNOO_SMILE_EMOJI = "<:snoo_smile:872943749972516885>"
TADA_EMOJI = EMOJIS[':party_popper:']
HYPE_EMOJI = "<:hype:872944748283969547>"
CALENDAR_EMOTE = EMOJIS[':calendar:']

ROLE_REACT_DICT1 = {
 GRYFFINDOR_EMOJI: GRYFFINDOR_ROLE_ID,
 HUFFLEPUFF_EMOJI: HUFFLEPUFF_ROLE_ID,
 RAVENCLAW_EMOJI: RAVENCLAW_ROLE_ID,
 SLYTHERIN_EMOJI: SLYTHERIN_ROLE_ID
}

ROLE_REACT_DICT2 = {
 EMOJIS[':brain:']: ELITE_ROLE_ID,
 EMOJIS[':crossed_swords:']: XPERT_ROLE_ID,
 EMOJIS[':chart_increasing:']: ADVANCE_ROLE_ID,
 EMOJIS[':person_walking:']: CASUAL_ROLE_ID,
 EMOJIS[':ogre:']: TROLL_ROLE_ID
}

################################################
################################################

# TESTING VALUES

# BOT_USER_ID = 794372617205317662
# DUELING_DISCORD_ID = 820327073213186079
# # ###############################
# # ###### CHANNEL IDS ############
# # ###############################
# ANNOUNCEMENTS_CHANNEL_ID = 826877242243809310
# LOBBY_CHANNEL_ID = 826877242243809310
# GAMEPLAY_CHANNEL_ID = 820347907449421875
# GAME_SIGNUPS_CHANNEL_ID = 820347907449421875
# BOT_LOG_CHANNEL_ID = 820347907449421875
# GAME_LOG_CHANNEL_ID = 826877242243809310
#
#
# # ###############################
# # ######### ROLE IDS ############
# # ###############################
#
# TRIVIA_TUESDAY_ROLE_ID = 873233509286813746
# CURRENT_PLAYER_ROLE_ID = 873591724667207701
#
# POTATO_ROLE_ID = 843656104385970196
# EAGLE_ROLE_ID = 843661105939218513
# CHEESE_ROLE_ID = 873003101743898634
# CHICKEN_ROLE_ID = 873003158949994509
# HOUSE_ROLES = [POTATO_ROLE_ID, EAGLE_ROLE_ID, CHEESE_ROLE_ID, CHICKEN_ROLE_ID]
#
# PIKA_ROLE_ID = 873028549391548446
# SQUIRT_ROLE_ID = 873028636649857035
# CHAR_ROLE_ID = 873028582786596946
# BULBA_ROLE_ID = 873028607465897994
# TAUROS_ROLE_ID = 873028662109282335
# TIER_ROLES = [PIKA_ROLE_ID, SQUIRT_ROLE_ID, CHAR_ROLE_ID, BULBA_ROLE_ID, TAUROS_ROLE_ID]
#
# # ###############################
# # ######### EMOJI IDS ###########
# # ###############################
#
# GENO_EMOJI = '<:angryGeno:842965440619610124>'
# THEW_EMOJI = '<:gottaGo:839282914051227649>'
# PAT_EMOJI = '<:thumbnail:842965702288998400>'
# COWBOY_EMOJI = '<:sadcowboy:842160471959666729>'
#
# SNOO_SMILE_EMOJI = '<:angryGeno:842965440619610124>'
# TADA_EMOJI = EMOJIS[':party_popper:']
# HYPE_EMOJI = '<:gottaGo:839282914051227649>'
# CALENDAR_EMOTE = EMOJIS[':calendar:']
#
# ROLE_REACT_DICT1 = {
#  GENO_EMOJI: POTATO_ROLE_ID, # potato
#  THEW_EMOJI: EAGLE_ROLE_ID, # eagle
#  PAT_EMOJI: CHEESE_ROLE_ID, # cheeese
#  COWBOY_EMOJI: CHICKEN_ROLE_ID # chicken
# }
# ROLE_REACT_DICT2 = {
#  EMOJIS[':brain:']: PIKA_ROLE_ID,
#  EMOJIS[':crossed_swords:']: SQUIRT_ROLE_ID,
#  EMOJIS[':chart_increasing:']: CHAR_ROLE_ID,
#  EMOJIS[':person_walking:']: BULBA_ROLE_ID,
#  EMOJIS[':ogre:']: TAUROS_ROLE_ID
# }
