%Paths to surface GIFTI files which supply vertex and face location
pathname = ''
addpath(sprintf('%s/gifti-master',pathname));
addpath(sprintf('%s/BrewerMap-master',pathname));
unf = gifti(sprintf('%s/tpl-avg_space-unfold_den-2k_midthickness.surf.gii',pathname));
FV = gifti(sprintf('%s/vertices_midsurf_L_mean.surf.gii',pathname));

%Assumes that the variable of interest to plot is called 'img' which has the same number of
%vertices defined in the surface files

    %is data continous or discrete?
    discrete = true;

    t = sort(img(:));
    t(isnan(t)) = [];
    
    if discrete
        window = [min(img),max(img)];
    else
        window = [t(round(length(t)*.05)) t(round(length(t)*.95))];
    end

        %% plot!
    figure('units','normalized','outerposition',[0 0 1 1]);
    subplot(1,2,1);
    x = size(img,3);
    p = patch('Faces',FV.faces,'Vertices',FV.vertices,'FaceVertexCData',img);
    p.FaceColor = 'flat';
    p.LineStyle = 'none';
    set(gca,'XColor',[1 1 1]); 
    set(gca,'yColor',[1 1 1]); 
    axis equal tight;
    if discrete
        map = brewermap(round(max(img)),'Set1');
        colormap(map); 
    end
    light;
    caxis(window);
    subplot(1,2,2);
    set(gca,'YDir');
    set(gca,'XDir');
    caxis(window);
    colorbar;
    
    p = patch('Faces',unf.faces,'Vertices',unf.vertices,'FaceVertexCData',img);
    p.LineStyle = 'none';
    p.FaceColor = 'flat';
    axis equal tight;   
    if discrete
        map = brewermap(round(max(img)),'Set1');
        colormap(map);  
    end 
    light;
    caxis(window);
    subplot(1,2,2);
    axis equal tight;
    camroll(90);
    set(gca,'YDir');
    set(gca,'XDir');
    set(gca,'XColor',[1 1 1]); 
    set(gca,'yColor',[1 1 1]); 
    caxis(window);
    colorbar;
    
