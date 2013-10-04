% Calculating the effects of dispersion

L = 2e-4; % length of fiber (km) [20cm]
lambda = 1220:1420; % wavelengths of interest (nm)
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

dispersion = zero_dispersion_slope*(1220:1:1420) - 1310*0.089;
% uncomment to have constant dispersion instead of variable
%dispersion = dispersion*0 + 5;


n_bk7 = zeros(1, length(dispersion));

for i = 1220:1:1420
    i_m = i * 1.0/1000;
    n_bk7(i-1219) = sqrt(1 + ...
        1.03961212*i_m^2/(i_m^2 - 0.00600069867) + ...
        0.231792344*i_m^2/(i_m^2 - 0.0200179144) + ...
        (1.01046945*i_m^2)/(i_m^2 - 103.560653));
end

n_bk7 = linspace(1, 10, length(n_bk7));
f = 1e9*c./lambda;

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

f_full = -5e14:1e8:5e14;

%7111268
%7457377

power_full = zeros(1, length(f_full));
power_full(7111268:7457377) = power_freq;

t_full_ext = ifftshift(ifft(fftshift(power_full)));

%figure(1)
%plot(abs(t_full_ext));

fwhm_no_dispersion = fwhm([(1:length(t_full_ext))' abs(t_full_ext)']);

disp(['FWHM w/o dispersion: ' num2str(fwhm_no_dispersion) ' fs'])

group_delay = cumtrapz(dispersion) + 0; % add arbitrary constant value
group_delay_freq = interp1(f, group_delay, f(end):1e8:f(1));

% ps / m
bk_7_group_delay_freq = interp1(f, inv_vg_bk7, f(end):1e8:f(1), 'spline');

phase_lag = 2*pi*L*cumtrapz(f(end):1e8:f(1), group_delay_freq*1e-12);
bk_7_phase_lag = 2*pi*L_bk_7*cumtrapz(f(end):1e8:f(1), bk_7_group_delay_freq*1e-12);

op = L_bk_7*n_bk7_freq;

op = ones(1, length(n_bk7_freq));

for i = 7111268:7457377
    bk_7_phase_lag(i-7111267) = (2*pi*f_full(i)/c)*op(i-7111267);
end

%phase_lag = zeros(1, length(inverse_vg_freq));

%for i = 1:length(inverse_vg_freq)
%    phase_lag(i) = 1e-12*2*pi*L*inverse_vg_freq(i)*(f_full(i+7111267));
%end

power_full_w_phase = power_full;

for i = 7111268:7457377
    power_full_w_phase(i) = power_full_w_phase(i)*exp(-1*sqrt(-1)* ...
        (bk_7_phase_lag(i-7111267)));%+phase_lag(i-7111267)));
end

t_full_ext_w_dispersion = fftshift((ifft(ifftshift(power_full_w_phase))));

%figure(2)
%plot(abs(t_full_ext_w_dispersion));

fwhm_w_dispersion = fwhm([(1:length(t_full_ext))' abs(t_full_ext_w_dispersion)']);

disp(['FWHM w/  dispersion: ' num2str(fwhm_w_dispersion) ' fs'])

disp(['FWHM distance w/o d: ' num2str(1e-15 * fwhm_no_dispersion * c * 1e6) ' microns'])
disp(['FWHM distance w/  d: ' num2str(1e-15 * fwhm_w_dispersion * c * 1e6) ' microns'])

disp(['Axial resolution FWHM w/o d: ' num2str(1e-15 * fwhm_no_dispersion * c * 1e6/2) ' microns'])
disp(['Axial resolution FWHM w/  d: ' num2str(1e-15 * fwhm_w_dispersion * c * 1e6/2) ' microns'])