import csv

# create list of all members
members = []
with open('member_bios.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for i, row in enumerate(csv_reader):
        if i != 0: # skip first row
            member = {}
            member['Name'] = row[1]
            member['Email'] = row[2]
            member['Year'] = row[3]
            member['Major/Minor'] = row[4]
            member['Hometown'] = row[5]
            member['Team'] = row[6]
            member['Favorite Sport(s)'] = row[7]
            member['Favorite Sport Team(s)'] = row[8]
            member['Fact'] = row[9]
            members.append(member)

# sort based on name
members = sorted(members, key = lambda i: i['Name'])


bio_snippet_1 = (
    "<div id=\"modal"
)

bio_snippet_2 = (
    "\" class=\"modal\">"
    "<div class=\"modal-content\">"
    "<img class=\"officer-images\" src=\"../assets/members_1819/\" alt=\"Avatar\">"
)

bio_snippet_3 = (
    "</div>"
    "<div class=\"modal-footer\">"
    "<a href=\"#!\" class=\"modal-action modal-close waves-effect waves-green btn-flat\">Return</a>"
    "</div>"
    "</div>"
)


member_card_1 = (
    "<div class=\"col s12 m6 l4\">"
        "<a class=\"modal-trigger\" href=\"#modal"
)

member_card_2 = (
    "\">"
    "<div class=\"card\">"
    "<div class=\"cardcontent\">"
    "<img class=\"officer-images\" src=\"../assets/members_1819/\" alt=\"Avatar\">"
    "<div class=\"cardcontainer\">"
)

member_card_3 = (
    "</div>"
    "</div>"
    "</div>"
    "</a>"
    "</div>"
)

# open existing officers file
with open('officers/index.html') as f:
    officer_file = f.read()


# get index to write into file
search_key = '<!-- begin bios -->'
write_index = officer_file.find(search_key)

# add in member bios
new_off = new_off = officer_file[:write_index + len(search_key)]
for i, member in enumerate(members):
    new_off += "\n"
    new_off += bio_snippet_1 + str(i + 10) + bio_snippet_2 + "\n"
    new_off += "<h4>" + member['Name'] + "</h4>" + "\n"
    new_off += "<p class=\"modal-text\">"
    new_off += "BSA Team: " + member['Team'] + "<br>"
    new_off += "Major/Minor: " + member['Major/Minor'] + "<br>"
    new_off += "Year: " + member['Year'] + "<br>"
    new_off += "Hometown: " + member['Hometown'] + "<br>"
    new_off += "Favorite Sport(s): " + member['Favorite Sport(s)'] + "<br>"
    new_off += "Favorite Sport Team(s): " + member['Favorite Sport Team(s)'] + "<br>"
    new_off += "Fun Fact: " + member["Fact"] + "<br><br>"
    new_off += "Contact: " + member["Email"]
    new_off += "</p>" + "\n" + bio_snippet_3 + "\n"


# member cards 
search_key = '<!-- begin cards -->'
write_index = officer_file.find(search_key)
last_chunk = officer_file[write_index + len(search_key):] # final part of file to attach later

cards = ""
for i, member in enumerate(members):
    cards += "\n"
    cards += member_card_1 + str(i + 10) + member_card_2 + "\n"
    cards += "<h4><b>" + member['Name'] + "</b></h4>" + "\n"
    cards += member_card_3 + "\n"

new_off += "\n" + search_key + "\n" + cards
new_off += last_chunk

print(new_off)