def download_file(name, file_link):
	"""
	Dowload file from link and save to local

	"""
    print("Download: "+file_link)
    file = requests.get(file_link, stream=True, headers=headers)
    file.raise_for_status()

    with open('{}/{}'.format(settings.DOWNLOADS_DIR, name), 'wb') as f:
        for block in file.iter_content(1024):
            f.write(block)
