# ftp (file transfer protocol) example

This is an example of transferring files to a ftp server.  

## Compatibility

Tested with:
  * Cloudify 5.0.5

## Requirements

In order to run this example, an ftp server should be configured.
Here is a [video guide](https://www.youtube.com/watch?v=FvOdeHlfM-Q) of configuring an aws EC2 instance to use as ftp server. 

   - [ ] install `cloudify-utilites-plugin`, see [releases](https://github.com/cloudify-incubator/cloudify-utilities-plugin/releases).

In order to run this example provide those inputs:
* ftp_ip - ftp server ip.
* ftp_user - ftp server user.
* ftp_password - ftp server user password
* ftp_port - ftp server port, by default 21.

**Example**:

`cfy install upload_ftp.yaml -i ftp_ip=<ip> -i ftp_user=<user_name>  -i ftp_password=<password>  -i=ftp_port=<port>`

