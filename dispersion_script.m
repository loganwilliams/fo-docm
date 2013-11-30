% Calculating the effects of dispersion

% TODO:
%   Cleanup/document the N-BK7 computations

L = 2e-4; % length of fiber (km) [20cm]
lambda = 1220:1420; % wavelengths of interest (nm)
f = 1e9*c./lambda; % frequencies of interest (hz)
zero_dispersion_slope = 0.089; % ps / (nm^2 km)
c = 2.998e8;
L_bk_7 = .04; % distance in N-BK7 glass (m) [4cm]

lambda_power = [1220 1240 1260 1280 1300 1320 1340 1360 1380 1400 1420];

% values taken from Exalos documentation for my specific SLD
%       1220 1240  1260  1280 1300 1320  1340  1360 1380 1400 1420
power = [-44 -30.5 -25.5 -23  -22  -21.5 -22.5 -25  -30  -40  -48];
%power = [-60  -60  -40   -20  -20  -20   -20   -20  -20  -40  -60];
power = interp1(lambda_power, power, lambda, 'spline');

power = 10.^(power./10);

fwhm_power = fwhm([lambda' power']);
disp(['FWHM power: ' num2str(fwhm_power) ' nm'])

dispersion = (zero_dispersion_slope*(1220:1:1420) - 1310*0.089)*L;

% dispersion is now in units of ps / nm
% [ps / nm]   <---????---> ps^2 (group delay dispersion)
% -lambda^2 / (2 * pi * c) * dispersion = [T^2]
% [nm^2] * [ps / nm] / ([m / s] * [nm/m] * [s / ps])
%   = [ps * nm] / [nm / ps] = [ps^2]

gdd = ((1220:1:1420).^2.*dispersion)/(2*pi*c*1e-12*1e9);

% units of group delay dispersion (gdd) are now in (ps)^2

% ZEMAX
% calculated GDD for other elements:    Third order
%   Fiber collimator: 10.78 (fs^2)      823.62 (fs^3)
%   GRIN lens:        58.49 (fs^2)      405.09 (fs^3)

tod = cumtrapz(f(end):1e8:f(1), ones(1, length(f(end):1e8:f(1))).* (823.62 - 405.09) * (1e-15)^3) * (1e12)^2;
tod_lambda = interp1(f(end):1e8:f(1), tod, f, 'spline');

gdd = gdd + (58.49 * (1e-3)^2) - (10.78 * (1e-3)^2);
gdd = gdd + tod_lambda;

% calculate the optical index of N-BK7 glass as a function of frequency

n_bk7 = zeros(1, length(dispersion));

for i = 1220:1:1420
    i_m = i * 1.0/1000;
    n_bk7(i-1219) = sqrt(1 + ...
        1.03961212*i_m^2/(i_m^2 - 0.00600069867) + ...
        0.231792344*i_m^2/(i_m^2 - 0.0200179144) + ...
        (1.01046945*i_m^2)/(i_m^2 - 103.560653));
end

%n_bk7 = linspace(1, 0, length(n_bk7)) + 1.5;

bk7_phase = L_bk_7 * 2 * pi * n_bk7 ./ (lambda*1e-9);

n_bk7_freq = interp1(f, n_bk7, f(end):1e8:f(1), 'spline');

dndl = diff(n_bk7);
dndl = [dndl(1) dndl];
vg_bk7 = c./(n_bk7 - (1220:1420) .* dndl);

% Try calculating the group velocity of n-bk7 glass using a slightly
% different method (this ends up returning almost exactly the same values)
dn_bk7 = diff(n_bk7_freq);
dn_bk7 = [dn_bk7(1) dn_bk7];
vg2_bk7 = (c./n_bk7_freq).*(1 - ((f(end):1e8:f(1))./n_bk7_freq).*(dn_bk7/1e8));

inv_vg_bk7 = 1e12./vg_bk7;

power_freq = interp1(f, power, f(end):1e8:f(1), 'spline');
bk7_phase_freq = interp1(f, bk7_phase, f(end):1e8:f(1), 'spline');

f_full = -5e14:1e8:5e14;

%7111268 - 1420 nm
%7457377 - 1220 nm

power_full = zeros(1, length(f_full));
power_full(7111268:7457377) = power_freq;

t_full_ext = ifftshift(ifft(fftshift(power_full)));

%figure(1)
%plot(abs(t_full_ext));

fwhm_no_dispersion = fwhm([(1:length(t_full_ext))' abs(t_full_ext)']);

disp(['FWHM w/o dispersion: ' num2str(fwhm_no_dispersion) ' fs'])

gdd_freq = interp1(f, gdd, f(end):1e8:f(1));
group_delay = cumtrapz(f(end):1e8:f(1), 2*pi*1e-12*gdd_freq);
phase_lag = cumtrapz(f(end):1e8:f(1), 2*pi*1e-12*group_delay);

bk_7_group_delay_freq = interp1(f, inv_vg_bk7, f(end):1e8:f(1), 'spline');



bk_7_phase_lag = 2*pi*L_bk_7*cumtrapz(f(end):1e8:f(1), bk_7_group_delay_freq*1e-12);

op = L_bk_7*n_bk7_freq;
bk_7_phase_lag = 2*pi.*f_full(7111268:7457377).*op./c;

%phase_lag = zeros(1, length(inverse_vg_freq));

%for i = 1:length(inverse_vg_freq)
%    phase_lag(i) = 1e-12*2*pi*L*inverse_vg_freq(i)*(f_full(i+7111267));
%end

power_full_w_phase = power_full;
bk_7_phase_lag = bk7_phase_freq;

power_full_w_phase(7111268:7457377) = power_full_w_phase(7111268:7457377).*exp(-1*sqrt(-1)* ...
     phase_lag(1:end));
        %(bk_7_phase_lag(1:end))+phase_lag(1:end));
        


t_full_ext_w_dispersion = fftshift((ifft(ifftshift(power_full_w_phase))));

%figure(2)
%plot(abs(t_full_ext_w_dispersion));

fwhm_w_dispersion = fwhm([(1:length(t_full_ext))' abs(t_full_ext_w_dispersion)']);

disp(['FWHM w/  dispersion: ' num2str(fwhm_w_dispersion) ' fs'])

disp(['FWHM distance w/o d: ' num2str(1e-15 * fwhm_no_dispersion * c * 1e6) ' microns'])
disp(['FWHM distance w/  d: ' num2str(1e-15 * fwhm_w_dispersion * c * 1e6) ' microns'])

disp(['Axial resolution FWHM w/o d: ' num2str(1e-15 * fwhm_no_dispersion * c * 1e6/2) ' microns'])
disp(['Axial resolution FWHM w/  d: ' num2str(1e-15 * fwhm_w_dispersion * c * 1e6/2) ' microns'])