import widgets as wd
import json
import requests
from webbrowser import open

# Generate a progress bar using emojis
def progressbar(raised, goal):
    # Modify these emoji to change the "empty" and "full" sections of the progress bar.
    progress_full = "🟩" 
    progress_empty = "⬜"
    bar_length = 12 # Modify this number to adjust the max width of the progress bar.
    progress_percent = float(raised)/float(goal)
    progress = ""
    progress = progress_full * int(bar_length * progress_percent)
    return '{:⬜<{x}}'.format(progress, x=bar_length) 
    #If you modify progress_empty above, you need to put it in this return statement as well.

# Configure the POST request to the Tiltify API, and return the JSON payload. The POST payload is atrocious, but in-line was better than having to configure external file references for people downloading this script!
headers = {"content-type": "application/json", "accept": "*/*"}
r = requests.post("https://api.tiltify.com", json = {
	"operationName": "get_campaign_by_vanity_and_slug",
	"variables": {"vanity": "@relay-fm", "slug": "relay-st-jude-21"},
	"query": "query get_campaign_by_vanity_and_slug($vanity: String, $slug: String) {     campaign(vanity: $vanity, slug: $slug) {       id       name       slug       status       originalGoal {         value         currency         __typename       }       region {         name         __typename       }       supportable       team {         id         avatar {           src           alt           __typename         }         name         slug         __typename       }       supportedCampaign {         team {           id           avatar {             src             alt             __typename           }           name           slug           __typename         }         avatar {           alt           height           width           src           __typename         }         name         slug         __typename       }       supportingCampaigns {         name         user {           id           username           slug           __typename         }         slug         avatar {           alt           src           __typename         }         goal {           value           currency           __typename         }         amountRaised {           value           currency           __typename         }         __typename       }       description       totalAmountRaised {         currency         value         __typename       }       goal {         currency         value         __typename       }       avatar {         alt         height         width         src         __typename       }       user {         id         username         slug         avatar {           src           alt           __typename         }         __typename       }       livestream {         type         channel         __typename       }       milestones {         id         name         amount {           value           currency           __typename         }         __typename       }       schedules {         id         name         description         startsAt         endsAt         __typename       }       rewards {         active         fulfillment         amount {           currency           value           __typename         }         name         image {           src           __typename         }         fairMarketValue {           currency           value           __typename         }         legal         description         id         startsAt         endsAt         quantity         remaining         __typename       }       challenges {         id         amount {           currency           value           __typename         }         name         active         endsAt         amountRaised {           currency           value           __typename         }         __typename       }       polls {         active         amountRaised {           currency           value           __typename         }         name         id         pollOptions {           name           id           amountRaised {             currency             value             __typename           }           __typename         }         __typename       }       cause {         id         name         slug         description         avatar {           alt           height           width           src           __typename         }         paymentMethods {           type           currency           sellerId           minimumAmount {             currency             value             __typename           }           __typename         }         paymentOptions {           currency           additionalDonorDetails           additionalDonorDetailsType           monthlyGiving           monthlyGivingMinimumAmount           minimumAmount           __typename         }         __typename       }       fundraisingEvent {         id         name         slug         avatar {           alt           height           width           src           __typename         }         paymentOptions {           currency           additionalDonorDetails           additionalDonorDetailsType           monthlyGiving           minimumAmount           __typename         }         monthlyGivingRewards {           active           amount {             currency             value             __typename           }           fairMarketValue {             currency             value             __typename           }           fulfillment           monthsToClaim           name           image {             src             __typename           }           description           id           startsAt           endsAt           legal           __typename         }         __typename       }       __typename     }     }"
}, headers = headers)


#Pull data from the returned JSON payload.
info = (r.json())
rawraised = info["data"]["campaign"]["totalAmountRaised"]["value"]
rawgoal = info["data"]["campaign"]["goal"]["value"]
# Convert pulled values into properly-formatted dollar values:
raised = "$" + '{0:,.2f}'.format(float(rawraised))
goal = "$" + '{0:,.2f}'.format(float(rawgoal))
bar = progressbar(rawraised, rawgoal) # Generate progress bar using raw values
progress =  str(round((float(rawraised)/float(rawgoal)*100),2)) + "%"


# Pyto Widget Magic (Most of this is directly from Pyto's example widget, and just modified to do what we need!)

if wd.link is None:
    widget = wd.Widget()
    wd.wait_for_internet_connection()
    background = wd.Color.rgb(219.7/255, 182.8/255, 72.2/255) 
    #You can modify the background color by altering the RGB values to your liking

    # Populate four rows of data, and accompanying font sizes:
    text1 = wd.Text("Raised: " + raised) 
    text1.font = wd.Font.bold_system_font_of_size(20)
    text2 = wd.Text("Goal: " + goal)
    text2.font = wd.Font.bold_system_font_of_size(20)
    text3 = wd.Text("Progress: " + progress)
    text3.font = wd.Font.bold_system_font_of_size(20)
    text4 = wd.Text(bar) #Progress bar
    text4.font = wd.Font.bold_system_font_of_size(18)
    
    # Supported layouts (the small widget is too small)
    layouts = [widget.medium_layout, widget.large_layout]
    for layout in layouts:
        layout.add_row([text1])
        layout.add_row([text2])
        layout.add_row([text3])
        layout.add_row([wd.Spacer()])
        layout.add_row([text4])
        layout.set_background_color(background)
        layout.set_link("https://stjude.org/relay")
    wd.schedule_next_reload(900) # Suggested refresh time in seconds
    wd.show_widget(widget)
else:
    open(wd.link) #This opens the link above when the widget is tapped.


