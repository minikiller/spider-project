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
    video_links = ['https://cdn-100.filestore.app/b6fc56da864b0/60f6d5ae37ec5/alternative_resolution_2510ae297451b_360p.mp4?temp_url_expires=1660003519&temp_url_id=f50fb32a-ddb6-43aa-9bf6-0d4674857872&countable=true&filename=1080P_4000K_251660312.mp4&inline=true&content_type=video%2Fmp4&concurrency=32&rate_limit=0&response_limit=0&ip_access_policy=first&tags=xf%3Axf%2Cvideo%3Avideo%2Cfull%3Afull%2C360p%3A360p%2Cwebapi%3Awebapi%2Cuser_file_id%3A0817ae558309c%2Cuser_id%3A&temp_url_issuer=5445f78a91de707b297e67ed&temp_url_sig=d08f996a35407db48ab7985fbe72448a4b9f3d223293089bc99aaa63b7c05bc014e9740f4d86f1e2d8c62011995105dc9db45b1ab470b9bb7aac76ac4b4cd2c8&client_ip=2601%3A589%3A4105%3A5086%3Abccd%3Aa0c%3A6510%3A6d39']
    #download all videos
    download_video_series(video_links)
