import os.path
import requests
import re
title = input('请输入短剧名称：')
if not os.path.exists(title): # 检查文件夹是否存在
    os.makedirs(title)        # 如果不存在，则创建文件夹
host_url = input('请输入短剧的网址：')
#https://www.kuaishou.com/short-video/3xmsgfhuwvfkwbc?authorId=3x9vz9wxjxxbcg4&streamSource=search&searchKey=%20%E5%85%AB%E7%99%BE%E5%9D%97%20%20%E4%B9%B0%E4%BA%86%E4%B8%AA%E4%BF%AE%E7%9C%9F%E7%95%8C&area=searchxxnull
#https://www.kuaishou.com/short-video/3xefgkz88gygeje?authorId=3xck5ghi8n7xfak&streamSource=search&searchKey=%20%E5%85%AB%E7%99%BE%E5%9D%97%20%20%E4%B9%B0%E4%BA%86%E4%B8%AA%E4%BF%AE%E7%9C%9F%E7%95%8C&area=searchxxnull
tubeId = re.findall('&tubeId=(.*?)&', host_url)[0]
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
url = 'https://www.kuaishou.com/graphql'
episodeNumber = 0
while True:
    data ={
        'operationName':'visionTubeEpisodeQuery',
        'query':'fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    verifiedDetail {\n      description\n      iconType\n      newVerified\n      musicCompany\n      type\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionTubeEpisodeQuery($tubeId: String, $episodeNumber: Int, $page: String, $channelId: Int, $webPageArea: String) {\n  visionTubeEpisode(tubeId: $tubeId, episodeNumber: $episodeNumber, page: $page, channelId: $channelId, webPageArea: $webPageArea) {\n    ...feedContent\n    result\n    status\n    __typename\n  }\n}\n',
        'variables': {'tubeId': tubeId, 'episodeNumber': episodeNumber, 'page': "theater", 'channelId': 0}
    }
    res = requests.post(url,headers=headers,json=data)
    down_url = re.findall('photoUrl":"(.*?)",', res.text)
    if not down_url:
        break
    print(down_url)
    down_res = requests.get(down_url[0],headers=headers)
    open(f'{title}/第{episodeNumber+1}集.mp4','wb').write(down_res.content)
    episodeNumber += 1
print("下载完成")
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips
# 把所有视频加载进来，保存在空列表中
video_clips = []
for i in range(1,episodeNumber+1):
    video = VideoFileClip(f'{title}/第{i}集.mp4')
    video_clips.append(video)
video_final = concatenate_videoclips(video_clips)
video_final.write_videofile(f'{title}/{title}-完整版.mp4')
