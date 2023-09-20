
import scratchattach as scratch3
import itertools, random, time, os

print("Logging in...")
try:
    session = scratch3.login("potatopotatopotato48", os.getenv["PASSWORD"])
    print("Sucessfully logged in!")
except Exception as error:
    print(f"Failed to log in. Error: {error}")


projects = ["894961375"]
ignore_list = []

def comments_from(p):
   steps = 0
   comments = []
   continuing = True
   while continuing:
       comment = p.comments(limit=1,offset=steps)
       if not comment == []:
           comments.append(comment)
           steps += 1
       else:
           continuing = False
           
   return comments


def replies_from(p,c):
   steps = 0
   comments = []
   continuing = True
   while continuing:
       comment = p.get_comment_replies(comment_id=c["id"], limit=1, offset=steps)
       if not comment == []:
           comments.append(comment)
           steps += 1
       else:
           continuing = False
           
   return comments



def replies_contains(p,c,text):
    replies = replies_from(p,c)
    for r in replies:
        reply = r[0]
        if text in reply["content"]:
            return True
    return False




#print(comments_from(session.connect_project(projects[0]))[0][0])
#print(replies_from(session.connect_project(projects[0]),comments_from(session.connect_project(projects[0]))[0][0]))
#print(replies_contains(session.connect_project(projects[0]),comments_from(session.connect_project(projects[0]))[0][0],"Don&apos;t advertise"))

print("Searching")
counter = 1

while True:
    for p in projects:
        project = session.connect_project(p)
        comments = comments_from(project)
        for c in comments:
            comment = c[0]
            if comment["id"] in ignore_list or replies_contains(project,comment,"Don&apos;t advertise"):
                if replies_contains(project,comment,"Don&apos;t advertise"):
                    ignore_list.append(comment["id"])
                continue
            else:

                ignore_list.append(comment["id"])
                if "scratch.mit.edu/projects/" in comment["content"]:
                    project.reply_comment(content=f"Don't advertise!\nI'm a bot, and this action was done automatically.\nRandom number to avoid spam: {random.randint(0,2000)}", parent_id=comment["id"], commentee_id=comment["author"]["id"])
                    print("Advertiser found!\nWaiting for cooldown...")
                    time.sleep(150)
                    print("Cooldown complete, searching!")
            project.update()
    counter += 1
    print(f"Cycle completed. Now on cycle {counter}")

            
