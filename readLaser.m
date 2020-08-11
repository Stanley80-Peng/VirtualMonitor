clear
clc


fold = '';
laser1File = [fold 'laser1Record.bin'];
laser2File = [fold 'laser2Record.bin'];


fid = fopen(laser1File, 'r');
count = 0;
%while ~feof(fid)

for i= 1:20000
       count = count +1;
       time_stamp(count,:) = fread(fid, 2, 'uint32');

       frame_id_length = fread(fid, 1, 'uint32');
       frame_id(count,:) = fread(fid, frame_id_length, 'char');

       angle_min(count,:) = fread(fid, 1, 'float');
       angle_max(count,:) = fread(fid, 1, 'float');
       angle_increment(count, :) = fread(fid, 1, 'float');
       time_increment(count, :) = fread(fid, 1, 'float');
       scan_time(count, :) = fread(fid, 1, 'float');
       range_min(count, :) = fread(fid, 1, 'float');
       range_max(count, :) = fread(fid, 1, 'float');
       ranges[count][:]

       rangs_length = fread(fid, 1, 'uint32');
       ranges(count, :) = fread(fid, rangs_length , 'float');

       intensities_length = fread(fid, 1, 'uint32');
       if intensities_length > 0
        intensities(count, :) = fread(fid, intensities_length , 'float');
       end


end

time = time_stamp(:,1) - time_stamp(1,1) +time_stamp(:,2)/1000000000;
time_interval=time(2:end) - time(1:end-1);
plot(time_interval);
figure;
hist(time_interval);
max(time_interval)
min(time_interval)
