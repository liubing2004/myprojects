package com.android.example.takepicture.takepicture;

import android.os.Environment;

/**
 * Created by bing on 1/18/15.
 */
public class Config {
 // File upload url (replace the ip with your server address)
    public static final String FILE_UPLOAD_URL = "http://10.0.2.2:8000/uploadpicture/";

    // Directory name to store captured images and videos
    public static final String IMAGE_DIRECTORY_NAME = "AndroidFileUpload";

    public final static String getImageDirectoryFullPath(){
        return Environment.getExternalStorageDirectory().toString()
                +"/Pictures/"+IMAGE_DIRECTORY_NAME;
    }
}
