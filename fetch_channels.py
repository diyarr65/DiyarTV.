import asyncio
import aiohttp
import json

# Optimize Edilmiş, Daha Hızlı ve Kararlı Kanal Listesi
raw_channels = [
    {
        "name": "TRT 1",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/TRT_1_logo_%282021-%29.svg/960px-TRT_1_logo_%282021-%29.svg.png",
        "url": "https://tv-trt1.medya.trt.com.tr/master.m3u8"
    },
    {
        "name": "TRT Haber",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/TRT_Haber_logo_%282021-%29.svg/960px-TRT_Haber_logo_%282021-%29.svg.png",
        "url": "https://tv-trthaber.medya.trt.com.tr/master.m3u8"
    },
    {
        "name": "TRT Çocuk",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/TRT_%C3%87ocuk_logo_%282021%29.svg/960px-TRT_%C3%87ocuk_logo_%282021%29.svg.png",
        "url": "https://tv-trtcocuk.medya.trt.com.tr/master.m3u8"
    },
    {
        "name": "NOW TV",
        "logo": "https://i.imgur.com/5EYjWK7.png",
        "url": "https://uycyyuuzyh.turknet.ercdn.net/nphindgytw/nowtv/nowtv.m3u8"
    },
    {
        "name": "ATV",
        "logo": "https://i.imgur.com/HyVUwFC.png",
        "url": "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/atv/atv_1080p.m3u8"
    },
    {
        "name": "TV 8",
        "logo": "https://upload.wikimedia.org/wikipedia/tr/thumb/6/68/Tv8_Yeni_Logo.png/960px-Tv8_Yeni_Logo.png",
        "url": "https://tv8.daioncdn.net/tv8/tv8.m3u8?app=7ddc255a-ef47-4e81-ab14-c0e5f2949788&ce=3"
    },
    {
        "name": "Habertürk TV",
        "logo": "https://i.imgur.com/6Tw3rUp.png",
        "url": "https://ciner-live.daioncdn.net/haberturktv/haberturktv.m3u8"
    },
    {
        "name": "Beyaz TV",
        "logo": "https://i.imgur.com/uykIdML.png",
        "url": "https://beyaztv.daioncdn.net/beyaztv/beyaztv.m3u8?app=fcd5c66b-da9d-44ba-a410-4f34805c397d&ce=3"
    },
    {
        "name": "Kanal 7",
        "logo": "https://i.imgur.com/0gq9xOm.png",
        "url": "https://kanal7-live.daioncdn.net/kanal7/kanal7.m3u8"
    },
    {
        "name": "A2TV",
        "logo": "https://iatv.tmgrup.com.tr/site/v2/a2tv/i/a2tv-logo.png",
        "url": "https://rnttwmjcin.turknet.ercdn.net/lcpmvefbyo/a2tv/a2tv.m3u8"
    },
    {
        "name": "TGRT Haber",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/TGRT_Haber_logo.png/600px-TGRT_Haber_logo.png",
        "url": "https://tgrt.medya.ihhlas.com.tr/tgrthaber/sdt/live.m3u8"
    }
]

TIMEOUT = 5.0

async def check_stream(session, channel):
    url = channel.get("url")
    try:
        async with session.get(url, timeout=TIMEOUT) as response:
            if response.status == 200:
                print(f"[ÇALIŞIYOR] {channel['name']}")
                return channel
    except Exception:
        pass
    print(f"[ÖLÜ/YAVAŞ] {channel['name']}")
    return None

async def filter_working_channels(all_channels):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [check_stream(session, ch) for ch in all_channels]
        results = await asyncio.gather(*tasks)
        return [ch for ch in results if ch is not None]

def main():
    print("Optimize kanallar test ediliyor...\n")
    working_channels = asyncio.run(filter_working_channels(raw_channels))
    
    with open("channels.json", "w", encoding="utf-8") as f:
        json.dump(working_channels, f, ensure_ascii=False, indent=4)
    
    js_content = f"window.channelData = {json.dumps(working_channels, ensure_ascii=False, indent=4)};"
    with open("channels.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"\nİşlem Tamamlandı! Toplam {len(working_channels)} kararlı kanal kaydedildi.")

if __name__ == "__main__":
    main()