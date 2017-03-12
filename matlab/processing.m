%http://blogs.mathworks.com/community/2014/10/06/acquire-data-from-device-sensors-with-matlab-mobile/
clc, clear all

filename = '../py/data/log/03_09_accelero.csv';
%data = readtable(filename);
%csv

fid = fopen(filename, 'rt')
C = textscan(fid,'%s %f %f %f %f %f %s', 'HeaderLines', 1, 'Delimiter',',');
fclose(fid);
x = C{2};
z = C{2};
y = C{4};
xyz = C{5};
time = C{6};

% Calculate and plot magnitude.
mag = sqrt(sum(x.^2 + y.^2 + z.^2, 2));

% Accounting for gravity.

magNoG2 = mag - mean(mag);

%Why is these different??
magNoG3 = mag;
magNoG = xyz;

% Plot magnitude.
plot(time, magNoG, 'b');
xlabel('Time (s)');
ylabel('Acceleration (m/s^2)');

% Use FINDPEAKS to determine the local maxima.
minPeakHeight = std(magNoG);
[pks, locs] = findpeaks(magNoG, 'MINPEAKHEIGHT', minPeakHeight);

% Fs = 3
% [pks, locs] = findpeaks(magNoG, Fs);

numSteps = numel(pks)

hold on;

% Place a red marker on the locations that correspond to peaks.
plot(time(locs), pks, 'r', 'Marker', 'v', 'LineStyle', 'none');
title('Counting Steps');
xlabel('Time (s)');
ylabel('Acceleration Magnitude, Gravity Removed (m/s^2)');
hold off;



%FFT, matlab webinar
