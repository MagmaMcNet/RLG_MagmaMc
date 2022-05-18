<?php

$homefolder = "./ServerData/";
$rootfolder = $homefolder . "__FILEZ__/";
$folder = $rootfolder.$_REQUEST['filename'];
if(!is_dir($homefolder)) {
    mkdir($rootfolder, 0777, true);
}
if(!is_dir($rootfolder)) {
    mkdir($rootfolder, 0777, true);
}
if(!is_dir(dirname($folder))) {
    mkdir(dirname($folder), 0755, true);
}
if($_REQUEST['filez'] == "write"){
    if( $_REQUEST["type"] != "a") {
        echo $_REQUEST['filename'];
        echo $_REQUEST['content'];
        if(is_file($folder)) {
            unlink($folder);
        }
        $a = fopen($folder, "c+");
        fclose($a);
        

        $a = fopen($folder, $_REQUEST["type"]."+");
    } else {
        if(!is_file($folder)) {
            $a = fopen($folder, "c+");
            fclose($a);
        }
        $a = fopen($folder, "a+");
    }
    fwrite($a, $_REQUEST['content']);
    fclose($a);
} elseif($_REQUEST['filez'] == "read") {
    if(is_file($folder)) {
        $b = fopen($folder, "r");
        echo fread($b, filesize($folder));
        fclose($b);
    } else {
        $b = fopen($folder, "c+");
        fwrite($b, "{}");
        echo "{}";
        fclose($b);
    }
} elseif($_REQUEST['filez'] == "scan") {
    if(!is_dir($folder)) {
        mkdir($folder, 0777, true);
    }
    if (is_dir($folder)) {
        if ($handle = opendir($folder)) {
            $scans = [];
            while (false !== ($entry = readdir($handle))) {
                if ($entry != "." && $entry != ".." && !is_dir($folder."/".$entry)) {
                    $scans[] = $entry;
                }
            }
            echo json_encode($scans);
            closedir($handle);
        }
    } else {
        echo "notexist";
    }
} elseif($_REQUEST['filez'] == "delete") {
    if(is_file($folder)) {
        unlink($folder);
    }
} elseif($_REQUEST['filez'] == "upload") {
    if(!is_dir(dirname($homefolder.$_REQUEST["filename"].$_FILES["file"]["name"]))) {
        mkdir(dirname($homefolder.$_REQUEST["filename"].$_FILES["file"]["name"]), 0777, true);
    }
    move_uploaded_file($_FILES["file"]["tmp_name"],$rootfolder.$_REQUEST["filename"].$_FILES["file"]["name"]);
    echo "done";
} elseif($_REQUEST["filez"] == "download") {
    $content = file_get_contents($rootfolder.$_REQUEST["filename"]);
    header('Content-Type: image/png');
    echo $content;
}

?>