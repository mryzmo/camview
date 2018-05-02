%this script will make a movie from co2 depletion files
% Dock all future figures
set(0,'DefaultFigureWindowStyle','docked')
close all
clear
%% files to read
temprange=[140 250 600]; %from 22 to 220 in 200 s. Used if no lv file
files.datafile='20171030_real_14.img'; frames=[1 35999];
profiles={
    '20171030_profile_8.img' 275
    '20171030_profile_10.img' 126
   % '20160805_profile_4.img' 200
    }; %[filenr temp; filenr temp]
profilepressure=300*.0143; %mbar in chanber. we had 20/80
files.reffile='';%2016-05-20_refcell3.txt'; %
files.lvfile='lv/2017-10-30_real26.txt';%2016-05-20_real3.txt';
files.msfile='lv/20171030_MS_14.asc';%MS_20160520_real3.asc';

%% load camera data (takes a few seconds or minutes)
%data=loadimg(.datafile,frames); %data to use

numavg=10; %number to average over
disp('Allocating memory...');
averageddata=zeros(256,256,ceil((frames(2)-frames(1))/numavg));
tic
disp(['Beginning to read ' files.datafile]);
for i=frames(1):numavg:frames(2)-numavg
averageddata(:,:,ceil(i/numavg))=mean(loadimgsilent(files.datafile,[i i+numavg-1]),3); %data to use
if mod(i-1,100*numavg)==0
    disp(['at frame ' num2str(i)])
end
end
toc
%% average over every x images
% numavg=10; %number to average over
% cut=mod(size(data,3),numavg); %number of frames to cut in the end
% %combine the pictures into a new 3d array
% if numavg>1 %only average if we actually want to
%     averageddata=squeeze(mean((reshape(data(:,:,cut+1:end),...
%         size(data,1),size(data,2),numavg,[])),3));
% else
%     averageddata=data;
% end
% clear cut;
% clear data;

%% the lines below will load the profiles
profiledata=zeros([size(averageddata(:,:,1)) size(profiles,1)]);
profileref=zeros(size(profiles,1),1);
for i=1:size(profiles,1)
profiledata(:,:,i)=meanimg(cell2mat(profiles(i,1)),[0 249]);
%scopetemp=load(cell2mat(profiles(i,3)));
%profileref(i)=mean(scopetemp(:,2));
end
profiledata(:,:,2)=profiledata(:,:,2)*1.2;

% make profile interpolation functions
%ptemp(temp) will give an profile at that temp
ptemp=@(temp) squeeze(interp1(cell2mat(profiles(:,2)),...
    permute(profiledata(:,:,:),[3 1 2]),temp,'linear','extrap'));
%ptemp=@(temp) 100;
%extrapolate the temperature
%tempi=@(frame) interp1([0 temprange(3)],temprange(1:2),...
%    frame/10,'linear','extrap'); %10 is from 10 Hz

%tempfake=@(frame) interp1([0 temprange(3)],temprange(1:2),...
%    frame/10,'linear','extrap'); %10 is from 10 Hz


%% load labview data, so temp & start time
if ~strcmp(files.lvfile,'')
    disp('Loading LabView data');
    labview=importdata(files.lvfile);
    starttime=datetime(labview.textdata(1))+seconds((frames(1)-1)/10);
    lvframe=@(framenr) find(labview.data(:,1)>framenr/10,1);
    labviewtemp=labview.data(lvframe(frames(1)):lvframe(frames(2)+20),3);
    tempi=@(frame) labviewtemp(lvframe(frame));
    tempaxis=linspace(frames(1),frames(2)+20,size(labviewtemp,1));
    figure(7)
    gasflow=labview.data(lvframe(frames(1)):lvframe(frames(2)+20),17:2:21);
    %plot(tempaxis,labviewtemp); hold on;
    plot(tempaxis,gasflow);
    title('Gas Flow')
    legend('CO','O_2','Ar');
    drawnow;
end
%% load ms data starting from the labview start time
if ~strcmp(files.msfile,'') || ~strcmp(files.lvfile,'')
    disp('Loading MS data...');
    if exist([files.datafile '_ms.mat'],'file')==2
        load([files.datafile '_ms.mat']);
    else
        [mstime,msspecies,mscurrents]=...
        loadms(files.msfile,starttime,frames(2)-frames(1)+1);
        save([files.datafile '_ms.mat'],'mstime','msspecies','mscurrents');
    end
    msaxis=linspace(frames(1),frames(2),size(mscurrents,1));
    getmsspecies=@(species) mscurrents(:,not(cellfun('isempty', ...
        strfind(msspecies,species))));
    figure(6);
    for i=1:length(msspecies)
        plot(msaxis,log(mscurrents(:,i))); hold on;
    end
    legend(msspecies)
end

%% calculate data
% this part divides by the profile and does the colnumn division thing
% check if settings regarding regions exists
if exist('settings.mat','file')==2
    load settings.mat;
end

if exist('rect','var')
        if any(strcmp('trend',fieldnames(rect)))
            trends=round(rect.trend);
            trend=zeros(size(averageddata,3),size(trends,1));
        end
        laser.upperedge=round(rect.laser(2));
        laser.loweredge=round(rect.laser(2)+rect.laser(4));
        laser.leftedge=round(rect.laser(1));
        laser.rightedge=round(rect.laser(1)+rect.laser(3));
        
end

divided=zeros(size(averageddata));
for i=1:size(averageddata,3)
    %cimg(:,:,i)=averageddata(:,:,i)./ptemp(tempi(i*numavg));
    cimg=averageddata(:,:,i)./ptemp(tempi(i*numavg))*profilepressure;
    meanbefore=mean(mean(cimg(laser.upperedge:laser.loweredge,:)));
    if exist('rect','var')
        meancol=smooth(mean(cimg(:,round(rect.div(1)):round(rect.div(1)+rect.div(3))),2),1);    
    else
    meancol=smooth(mean(cimg(:,[1:15]),2),1);
    end
    divided(:,:,i)=cimg(:,:);
    %divided(:,:,i)=bsxfun(@rdivide, cimg(:,:),meancol);
    meanafter=mean(mean(divided(laser.upperedge:laser.loweredge,:,i)));
    divided(:,:,i)=divided(:,:,i)*(meanbefore/meanafter);
    if exist('trends','var')
        for t=1:size(trends,1)
            trend(i,t)=mean(mean(divided(trends(t,2):trends(t,2)+trends(t,4),...
                trends(t,1):trends(t,1)+trends(t,3),i)));
            %trend(i,t)=mean(mean(cimg(trends(t,2):trends(t,2)+trends(t,4),...
                %trends(t,1):trends(t,1)+trends(t,3))));
        end
    end
end

%% show data
mkdir('Vid')
%times=[2200 2800];
times=[1 3600];

%v = VideoWriter(['Vid/' num2str(files.datafile) '-' num2str(numavg) 'avg' '.fig'],'Uncompressed AVI');open(v);
colors=lines(10);
figure(1)
    subplot(3,2,4) %MS
    plot(msaxis/10,getmsspecies('44')/max(getmsspecies('44')));%*max(labviewtemp));
    xlim(times)
    %hold on;
    xlabel('time [s]');
    %plot(tempaxis,labviewtemp);
    title(strrep(num2str(files.msfile),'_','\_'));
    %legend('MS','Temp','Location','northwest');
%for i=10*times(1)/numavg:10*times(2)/numavg
for i=3100*10/numavg
    subplot(3,2,1) %PLIF Image
    if exist('laser','var')
        %draw image 
        imagesc(divided(laser.upperedge:laser.loweredge,laser.leftedge:laser.rightedge,i),...
            [0 1]*profilepressure)
        %imagesc(divided(laser.upperedge:laser.loweredge,:,i),...
        %    [0 .7])
        %draw lower rectangle
        rectangle('Position',...
            [0 laser.loweredge-laser.upperedge, laser.rightedge-laser.leftedge 10],...
            'FaceColor','black');
        %draw catalyst
        rectangle('Position',...
            [rect.catalyst(1) laser.loweredge-laser.upperedge, rect.catalyst(3) 10],...
            'FaceColor','white');
    else
        imagesc(divided(110:190,:,i),[0.5 5]*profilepressure)
    end
    colorbar('southoutside')
    %We have 11.1 px / mm
    catacenter=round(rect.catalyst(1)+rect.catalyst(3)/2);
    catasize=8; scale=rect.catalyst(3)/catasize;
    xticks=[catacenter:-scale*3:0 catacenter+3*scale:scale*3:256];
    set(gca,'XTick',sort(xticks));
    set(gca,'XTickLabel',sort((xticks-catacenter)./scale));
    yticks=sort(laser.loweredge-laser.upperedge:-scale*2:0);
    set(gca,'YTick',yticks);
    set(gca,'YTickLabel',sort(yticks-(laser.loweredge-laser.upperedge))./11.1);
    ylabel('y [mm]');xlabel('x [mm]')
    axis image    
    colormap jet

    subplot(3,2,2) %PLIF Trend
    if exist('trend','var')
            subplot(3,2,1) 
          for t=1:size(trend,2) %PLIF Image
            rectangle('Position',trends(t,:)-[0 laser.upperedge 0 0],...
                'EdgeColor',colors(t,:),'LineWidth',1.5);
          end
     subplot(3,2,2) %PLIF Trend
    for t=1:size(trend,2)
        plot(linspace(frames(1)/10,frames(2)/10,length(trend(:,t))),trend(:,t))
        hold all;
        xlim(times)
    end
    xlabel('time [s]');
    ylabel('CO_2 pressure [mbar]')
    title(char(starttime));
    ylim([0 max(max(trend))]); %xlim([0 size(averageddata,3)])
    end
    
    rectangle('Position',[i/10*numavg,0,1,6])
    
    hold off
    
    
    subplot(3,2,6) 
    load('lv/refl14trend.mat')
    plot(trendbox);ylim([.9 .96])
    xlim(times);
    title('refl14.sif');
    
    subplot(3,2,[3,5]);
    imshow(rand(100));
    %imshow(['new_oscillations_7_jpeg/new_oscillations_' num2str(70000+2*i) '.jpg'],'InitialMagnification', 'fit');
    
    %writeVideo(v,getframe(gcf))
end
mkdir('Fig')
subplot(3,2,1)
title([strrep(num2str(files.datafile),'_','\_'),', ' num2str(numavg) 'avg'])

savefig(['Fig/' num2str(files.datafile) '-' num2str(numavg) 'avg' '.fig']);
%close(v);
%%
system(['ffmpeg -i Vid/output.avi -c:v libx264 -preset slow -crf 15 -c:a copy ' 'Vid/' num2str(files.datafile) '-' num2str(numavg) 'avg' '.mp4']);
system('rm Vid/output.avi');
%print('Samsung-CLP-320-Series');
%%
%% look at the profile
% for i=120:250
%     profile=ptemp(i);
%     subplot(2,1,1)
%    imagesc(profile,[0 100]);
%    subplot(2,1,2)
%    plot(profile(125,:))
%    xlim([0 256]);
%     drawnow;
%  end

load('sxrd14.mat');
plot(sxrd14.reg2(1:2:end)/max(sxrd14.reg2(1:2:end)));hold all;
plot(sxrd14.reg4(1:2:end)/max(sxrd14.reg4(1:2:end)))
plot(sxrd14.reg6(1:2:end)/max(sxrd14.reg6(1:2:end)))
plot(sxrd14.reg8(1:2:end)/max(sxrd14.reg8(1:2:end)))
