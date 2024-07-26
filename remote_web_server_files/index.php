<?php
header('Content-Type: application/json');

// Get the 'folder_name' parameter from the query string
$folder_name = isset($_GET['folder_name']) ? $_GET['folder_name'] : '';

// Determine the directory to scan
$directory = $folder_name ? __DIR__ . DIRECTORY_SEPARATOR . $folder_name : __DIR__;

// Initialize an array to hold the folder names and their files
$folders = [];

// Check if the specified directory exists and is a directory
if (is_dir($directory)) {
    // Open the directory
    if ($handle = opendir($directory)) {
        // Loop through the directory contents
        while (false !== ($entry = readdir($handle))) {
            // Check if the entry is a directory and not '.' or '..'
            if ($entry != '.' && $entry != '..' && is_dir($directory . DIRECTORY_SEPARATOR . $entry)) {
                $subfolder_path = $directory . DIRECTORY_SEPARATOR . $entry;
                $files = [];

                // Open the subfolder
                if ($sub_handle = opendir($subfolder_path)) {
                    // Loop through the subfolder contents
                    while (false !== ($sub_entry = readdir($sub_handle))) {
                        // Check if the entry is a file and not '.' or '..'
                        if ($sub_entry != '.' && $sub_entry != '..' && is_file($subfolder_path . DIRECTORY_SEPARATOR . $sub_entry)) {
                            $files[] = $sub_entry;
                        }
                    }
                    // Close the subfolder handle
                    closedir($sub_handle);
                }

                // Add the subfolder and its files to the folders array
                $folders[$entry] = $files;
            }
        }
        // Close the directory handle
        closedir($handle);
    }
}

// If the specified directory does not exist, return an empty dictionary
if (empty($folders) && !is_dir($directory)) {
    echo json_encode(new stdClass());
} else {
    // Output the folder names and their files as a JSON object
    echo json_encode($folders);
}
?>
