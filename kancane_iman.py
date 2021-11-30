import pytube
def ytdw(url,pilext):
    youtube = pytube.YouTube(url)
    if pilext=='v':
        pilres = str(input("Masukkan resolusi video [144p, 240p, 720p, etc.] : "))
        print("Sedang mengunduh...")
        youtube.streams.filter(res=pilres,only_audio=False).first().download('./unduhan')
    else:
        print("Sedang mengunduh...")
        youtube.streams.filter(only_audio=True).first().download('./unduhan')
    print("Unduhan selesai.\n")
    print("Penulis : Iman Widayat")
    print("Credit : https://pytube.io > library\n")
    print("----------------------------------------------------------------------------------\n")
if __name__ == '__main__':
    print("----------------------------------------------------------------------------------\n")
    print("Python YouTube Downloader, CTRL+C untuk keluar\n")
    url = str(input("Masukkan URL/Link video : "))
    pilext = str(input("Masukkan 'v' untuk mengunduh video atau 'a' untuk audio saja : "))
    ytdw(url,pilext)