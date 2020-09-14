import requests
import json
from PIL import ImageTk, Image
from io import BytesIO
from datetime import datetime, timezone
import tkinter.messagebox
import socket
from urllib.parse import urlparse, parse_qs
import webbrowser
import tkinter as tk

LOAD_IMAGES = True

class commentFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.commentData = kwargs.pop("data")
        tk.Frame.__init__(self, *args, **kwargs)
        self.config()
        self.authorImgFrm = tk.Frame(self)
        self.authorImgFrm.grid(row = 0, column = 0, rowspan = 3)
        if LOAD_IMAGES:
            imageData = requests.get(self.commentData["authorImg"])
            tkImg = ImageTk.PhotoImage(Image.open(BytesIO(imageData.content)))
            self.image = tkImg
            self.authorImgLab = tk.Label(self.authorImgFrm, image = tkImg)
            self.authorImgLab.pack()
        else:
            self.authorImgFrm.config(bg = "black", height = 40, width = 40)
        self.topFrm = tk.Frame(self)
        self.topFrm.grid(row = 0, column = 1, sticky = "nesw")
        self.authorLab = tk.Label(self.topFrm, text = self.commentData["author"])
        self.authorLab.pack(side = "left", ipadx = 5, ipady = 2)
        dateObj = datetime.strptime(self.commentData["date"], "%Y-%m-%dT%H:%M:%SZ")
        if dateObj.date() == datetime.today().date():
            formatCode = "%H:%M"
        else:
            formatCode = "%#d %b %Y"
        formattedDate = datetime.strftime(dateObj, formatCode)
        self.dateLab = tk.Label(self.topFrm, text = formattedDate)
        self.dateLab.pack(side = "right", ipadx = 5, ipady = 2)
        self.commentFrm = tk.Frame(self)
        self.commentFrm.grid(row = 1, column = 1, sticky = "nesw")
        self.commentLab = tk.Label(self.commentFrm, text = self.commentData["text"], wraplength = 500, anchor = "e", justify = "left")
        self.commentLab.pack(side = "left", ipadx = 5, ipady = 2)
        self.likeFrm = tk.Frame(self)
        self.likeFrm.grid(row = 2, column = 1, columnspan = 2, sticky = "nesw")
        self.likeLab = tk.Label(self.likeFrm, text = "{:,} like{}".format(self.commentData["likes"], "s" if self.commentData["likes"] > 1 else ""))
        self.likeLab.pack(side = "right")
        self.div = tk.Frame(self, height = 1, bg = "grey")
        self.div.grid(row = 3, columnspan = 3, sticky = "ew")
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 100)

class ytCommentsViewer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #Check internet connection
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        except socket.error:
            tk.messagebox.showerror("No connection","Could not connect to the Internet. Internet connection reuqired")
            self.destroy()
        else:
            self.title("YouTube Comment Viewer")
            self.geometry("600x700")
            self.resizable(False, True)
            self.topFrm = tk.Frame(self)
            self.topFrm.pack(padx = 10, pady = 10, fill = "both")
            self.loadFrm = tk.Frame(self.topFrm)
            self.loadFrm.pack(fill = "both")
            self.urlLab = tk.Label(self.loadFrm, text = "Enter youtube video URL:")
            self.urlLab.grid(row = 0, column = 0, sticky = "e")
            self.urlEnt = tk.Entry(self.loadFrm)
            self.urlEnt.grid(row = 0, column = 1, columnspan = 2, padx = 10, sticky = "nesw")
            self.urlEnt.focus()
            self.urlBtn = tk.Button(self.loadFrm, text = "Load comments", command = self.validateAndLoad)
            self.urlBtn.grid(row = 0, column = 3)
            self.urlNumLab = tk.Label(self.loadFrm, text = "Number of comments to load:")
            self.urlNumLab.grid(row = 1, column = 0, sticky = "e")
            self.urlNumEnt = tk.Entry(self.loadFrm, width = 4)
            self.urlNumEnt.insert(0, 25)
            self.urlNumEnt.grid(row = 1, column = 1, sticky = "nsw", padx = 10, pady = 5)
            self.urlErr = tk.Label(self.loadFrm, text = "")
            self.urlErr.grid(row = 1, column = 2, columnspan = 2, sticky = "w")
            self.loadFrm.grid_columnconfigure(0, weight = 1)
            self.loadFrm.grid_columnconfigure(1, weight = 6)
            self.loadFrm.grid_columnconfigure(2, weight = 6)
            self.loadFrm.grid_columnconfigure(3, weight = 1)
            self.div2 = tk.Frame(self, height = 3, bg = "black")
            self.div2.pack(fill = "x")
            self.mainWrap = tk.Frame(self)
            self.mainWrap.pack(fill = "both", expand = True)
            self.cnvWrap = tk.Canvas(self.mainWrap, highlightthickness = 0)
            self.cnvWrap.pack(side = "left", expand = True, fill = "both")
            self.mainFrm = tk.Frame(self.cnvWrap)
            self.mainFrm.bind("<Configure>", self.canvasConfig)
            self.mainFrmWindow = self.cnvWrap.create_window((0,0), window= self.mainFrm, anchor = "nw")
            self.cnvScroll = tk.Scrollbar(self.mainWrap, orient = "vertical", command = self.cnvWrap.yview)
            self.cnvScroll.pack(side = "right", fill = "y")
            self.cnvWrap.configure(yscrollcommand = self.cnvScroll.set)
            self.bind("<MouseWheel>", self.scrollWheel)
    def getIdFromUrl(self, url):
        query = urlparse(url)
        if query.hostname == 'youtu.be': return query.path[1:]
        if query.hostname in {'www.youtube.com', 'youtube.com'}:
            if query.path == '/watch': return parse_qs(query.query)['v'][0]
            if query.path[:7] == '/embed/': return query.path.split('/')[2]
            if query.path[:3] == '/v/': return query.path.split('/')[2]
        return None
    def validateAndLoad(self):
        userUrl = self.urlEnt.get()
        userNum = self.urlNumEnt.get()
        try:
            int(userNum)
        except:
            self.urlErr.config(text = "Enter an integer for comment number", fg = "red")
        else:
            if int(userNum) > 100:
                self.urlErr.config(text = "Maximum number of comments: 100", fg = "red")
            else:
                self.videoId = self.getIdFromUrl(userUrl)
                if self.videoId  == None:
                    self.urlErr.config(text = "Invalid YouTube URL", fg = "red")
                else:
                    self.urlErr.config(text = "Loading...", fg = "black")
                    self.update()
                    try:
                        self.videoDataRaw = requests.get("https://www.googleapis.com/youtube/v3/videos?part=snippet&id={}&key=AIzaSyA3h9KUMDVG2Bv5iqt_Fpd21nkr1pYGsB0".format(self.videoId)).json()["items"][0]["snippet"]
                    except:
                        self.urlErr.config(text = "Can't get data for that video", fg = "red")
                    else:
                        self.statsDataRaw = requests.get("https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key=AIzaSyA3h9KUMDVG2Bv5iqt_Fpd21nkr1pYGsB0".format(self.videoId)).json()["items"][0]["statistics"]
                        self.commentNumber = userNum
                        self.commentDataRaw = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyA3h9KUMDVG2Bv5iqt_Fpd21nkr1pYGsB0&textFormat=plainText&part=snippet&videoId={}&maxResults={}&order=relevance".format(self.videoId, self.commentNumber)).json()["items"]
                        self.commentData = []
                        for i in self.commentDataRaw:
                            d = i["snippet"]["topLevelComment"]["snippet"]
                            self.commentData.append({"author": d["authorDisplayName"], "authorImg": d["authorProfileImageUrl"], "likes": d["likeCount"], "date": d["publishedAt"], "text": d["textDisplay"]})
                        self.videoData = {"title": self.videoDataRaw["title"], "channel": self.videoDataRaw["channelTitle"], "thumbUrl": self.videoDataRaw["thumbnails"]["default"]["url"], "likes": self.statsDataRaw["likeCount"], "views": self.statsDataRaw["viewCount"], "published": self.videoDataRaw["publishedAt"]}
                        self.loadFrm.pack_forget()
                        self.urlEnt.delete(0, "end")
                        self.urlNumEnt.delete(0, "end")
                        self.urlNumEnt.insert(0, 25)
                        self.urlErr.config(text = "")
                        self.infoFrm = tk.Frame(self.topFrm)
                        self.infoFrm.pack(fill = "both")
                        thumbReq = requests.get(self.videoData["thumbUrl"])
                        tkThumb = ImageTk.PhotoImage(Image.open(BytesIO(thumbReq.content)))
                        self.thumbImage = tkThumb
                        self.infoThumb = tk.Label(self.infoFrm, image = tkThumb)
                        self.infoThumb.grid(row = 0, column = 0, rowspan = 5)
                        self.infoTitle = tk.Label(self.infoFrm, text = self.videoData["title"], font = "-weight bold", wraplength = 300)
                        self.infoTitle.grid(row = 0, column = 1, padx = 10)
                        self.infoChannel = tk.Label(self.infoFrm, text = self.videoData["channel"])
                        self.infoChannel.grid(row = 1, column = 1)
                        self.infoLikeviews = tk.Label(self.infoFrm, text = "{:,} views    {:,} likes".format(int(self.videoData["views"]), int(self.videoData["likes"])))
                        self.infoLikeviews.grid(row = 2, column = 1)
                        dateObj = datetime.strptime(self.videoData["published"], "%Y-%m-%dT%H:%M:%SZ")
                        dateStr = datetime.strftime(dateObj, "%#d %b %Y") 
                        self.infoDate = tk.Label(self.infoFrm, text = "Published {}".format(dateStr))
                        self.infoDate.grid(row = 3, column = 1)
                        self.infoNum = tk.Label(self.infoFrm, text = "Showing first {} comments ordered by relevance".format(self.commentNumber))
                        self.infoNum.grid(row = 4, column = 1)
                        self.infoFrm.grid_columnconfigure(0, weight = 2)
                        self.infoFrm.grid_columnconfigure(1, weight = 4)
                        self.infoFrm.grid_columnconfigure(2, weight = 1)
                        self.infoLoadNew = tk.Button(self.infoFrm, text = "Load another video", command = self.loadAnother)
                        self.infoLoadNew.grid(row = 1, column = 2, sticky = "nesw", pady = 10)
                        self.infoOpen = tk.Button(self.infoFrm, text = "Open video", command = self.openVideo)
                        self.infoOpen.grid(row = 2, column = 2, sticky = "nesw")
                        self.dcCont = True
                        self.displayComments()
    def loadAnother(self):
        self.dcCont = False
        self.infoFrm.pack_forget()
        for c in self.mainFrm.winfo_children():
            c.destroy()
        self.cnvWrap.yview_moveto(0)
        self.loadFrm.pack(fill = "both")
    def openVideo(self):
        webbrowser.open("https://youtu.be/{}".format(self.videoId))
    def scrollWheel(self, event):
        self.cnvWrap.yview_scroll(int(-1*(event.delta/120)), "units")
    def displayComments(self):
        for i in self.commentData:
            if self.dcCont:
                cf = commentFrame(self.mainFrm, data = i)
                cf.pack(fill = "x", pady = 2)
                self.update()
    def canvasConfig(self, event):
        self.cnvWrap.config(scrollregion = self.cnvWrap.bbox("all"))
        self.cnvWrap.itemconfig(self.mainFrmWindow, width = self.cnvWrap.winfo_width())

app = ytCommentsViewer()
app.mainloop()
