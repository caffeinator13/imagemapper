import PIL
import PIL.Image
import PIL.ExifTags
#import exifread




def get_loc(image):
	try:
		img = PIL.Image.open(image)
		
		exif_data = img._getexif()
		exif = {
	    PIL.ExifTags.TAGS[k]: v
	    for k, v in img._getexif().items()
	    if k in PIL.ExifTags.TAGS
		}
		if 'GPSInfo' in exif.keys():
			try:
				lat_tup = exif['GPSInfo'][2]
				long_tup = exif['GPSInfo'][4]
				lat_d = float(lat_tup[0][0])/float(lat_tup[0][1])
				lat_m = float(lat_tup[1][0])/float(lat_tup[1][1])/float(60)
				lat_s = float(lat_tup[2][0])/float(lat_tup[2][1])/float(3600)
				long_d = float(long_tup[0][0])/float(long_tup[0][1])
				long_m = float(long_tup[1][0])/float(long_tup[1][1])/float(60)
				long_s = float(long_tup[2][0])/float(long_tup[2][1])/float(3600)

				lat = lat_d + lat_m + lat_s
				lon = long_d + long_m + long_s
				gps_info = [lat,lon]
			except:
				gps_info = 'A'
		else:
			gps_info = 'A'
	except:
		gps_info = 'A'
	return gps_info


#get_loc("dude.jpg")