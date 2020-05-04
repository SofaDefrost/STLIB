function UDP_controller(ip,port_in, port_out)
%UDPController enables UDP communication.
%
%   TODO : for now works with 'schar' format, but precision is not enough

%% init udp
udp_obj_in = udp(ip,port_out,'LocalPort',port_in);
fopen(udp_obj_in);

udp_obj_out = udp(ip,port_out);
fopen(udp_obj_out);

cleanupObj = onCleanup(@()cleanMeUp(udp_obj_in, udp_obj_out));

%% main routine
while(1)
    % send data
    fwrite(udp_obj_out,6,'schar');
    % receive data
    [command,count] = fread(udp_obj_in,1,'schar');
    if isequal(count,0)
        warning('[%s] %s', mfilename, 'Received nothing from UDP port.');
    else
        disp(command);
    end
end

end


function cleanMeUp(udp_obj_in, udp_obj_out)
warning('[%s] %s', mfilename, 'CLosing UDP communication...');
fclose(udp_obj_in);
delete(udp_obj_in);
fclose(udp_obj_out);
delete(udp_obj_out);
warning('[%s] %s', mfilename, 'UDP communication closed.');
end

