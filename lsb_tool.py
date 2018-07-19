from PIL import Image
import sys

end_of_msg = 'end_of_msg'

def str2bin( string ):
	res = ''

	for i in string:
		_binChar = bin( ord( i ) )[2:]
	
		while len( _binChar ) != 8:
			_binChar = '0' + _binChar
		
		res += _binChar                                
	
	return res

def int2bin( num ):
	res = ''
	res = bin( num )[2:]

	while len( res ) != 8:
		res = '0' + res

	return res

def writeMsg( filename ):
	img = Image.open( filename )
	size = img.size
	x_border = size[ 0 ]
	maxMsgSize = ( ( size[ 0 ] * size[ 1 ] * 6 ) / 8 ) - len( end_of_msg ) 

	message = ''
	
	cord_x = 0
	cord_y = 0
	colorNum = 0

	print "Max message size is %d bytes" % maxMsgSize
	print "Choice the option\n1. Enter the message\n2. Read from file"
	option = raw_input( "Option: " )

	if option == '1':
		message = raw_input( "Enter the message: " )
		if len( message ) > maxMsgSize:
			print "[-] Message size is to big"
			sys.exit( -1 )

	elif option == '2':
		inputFileName = raw_input( "Enter the filename: " )

		try:
			fd = open( inputFileName, 'rb' )
		except:
			print "[-] File open error!"
			sys.exit( -1 )
		
		message = fd.read()
		fd.close()

		if len( message ) > maxMsgSize:
			print "[-] File size is to big"
			sys.exit( -1 )

	else:
		print "[-] Invalid option!"
		sys.exit( -1 )

	pixels = img.load()
	message += end_of_msg

	message = str2bin( message )
	
	for i in range( 0, len( message ), 2 ):

		_pixelVal = pixels[ cord_x, cord_y ][ colorNum ]

		_pixelVal = int2bin( _pixelVal )

		_pixelVal = list( _pixelVal )

		_pixelVal[ 6 ] = message[ i ]
		_pixelVal[ 7 ] = message[ i + 1 ]

		_pixelVal = "".join( _pixelVal )

		_pixelVal = int( _pixelVal, 2 )

		if colorNum == 0:
			pixels[ cord_x, cord_y ] = ( _pixelVal, 
				pixels[ cord_x, cord_y ][ 1 ], 
				pixels[ cord_x, cord_y ][ 2 ] )

		elif colorNum == 1:
			pixels[ cord_x, cord_y ] = ( pixels[ cord_x, cord_y ][ 0 ], 
				_pixelVal,
				pixels[ cord_x, cord_y ][ 2 ] )

		elif colorNum == 2:
			pixels[ cord_x, cord_y ] = ( pixels[ cord_x, cord_y ][ 0 ], 
				pixels[ cord_x, cord_y ][ 1 ], _pixelVal )

		colorNum += 1

		if colorNum > 2:
			cord_x += 1
			colorNum = 0

		if cord_x >= x_border:
			cord_y += 1
			cord_x = 0

	out_img = Image.new( img.mode, img.size )
	pixelsNew = out_img.load()

	for i in range( img.size[ 0 ] ):
		for j in range( img.size[ 1 ] ):
			pixelsNew[ i, j ] = pixels[ i, j ]

	img.close()

	out_img.save( "enc_" + filename.split( '.' )[ 0 ] + ".png" )
	out_img.close()

def readMsg( filename ):
	img = Image.open( filename )

	pixels = img.load()
	size = img.size

	res = ''
	readed = ''

	for i in range( 0, size[ 1 ] ):
		for j in range( 0, size[ 0 ] ):
			for k in range( 3 ):
				if pixels[ j, i ][ k ] == 0:
					res += "00"

				elif pixels[ j, i ][ k ] == 1:
					res += "01"
				else:
					res += bin( pixels[ j, i ][ k ] )[-2:]

				if len( res ) == 8:
					readed += chr( int( res, 2 ) )
					res = ''

					if end_of_msg in readed:
						break
			
	readed = readed.split( end_of_msg )[ 0 ]
	fd = open( 'readMsg.txt', 'wb' )
	fd.write( readed )
	fd.close()

if __name__ == "__main__":
	if len( sys.argv ) > 2:
		filename = sys.argv[ 1 ]
		mode = sys.argv[ 2 ]
	else:
		print "Usage python stegoLSB.py <file> <read/write>"
		sys.exit( -1 )

	if mode == 'write':
		writeMsg( filename )

	elif mode == 'read':
		readMsg( filename )

	else:
		print "Error in mode value!"
		sys.exit( -1 )
