import requests
def download_video_series(video_links):

    for link in video_links:

        # iterate through all links in video_links
        # and download them one by one
        #obtain filename by splitting url and getting last string
        file_name = link.split('/')[-1]

        print("Downloading file:%s" % file_name)

        #create response object
        r = requests.get(link, stream=True)

        #download started
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    print("Downloading %s" % file_name)
                    f.write(chunk)

        print("%s downloaded!\n" % file_name)

    print("All videos downloaded!")
    return


if __name__ == "__main__":
  #getting all video links
#   video_links = get_video_links()
    video_links = ['https://www.tgbak.com/pornhub/Horny%20Kira/HE%20CUMSHOT%20ON%20MY%20SCHOOL%20DRESS%21.mp4']
    #download all videos
    download_video_series(video_links)
