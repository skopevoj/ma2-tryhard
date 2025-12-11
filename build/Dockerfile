FROM nginx:alpine

# Copy the HTML file, favicon and images to nginx html directory
COPY index.html /usr/share/nginx/html/
COPY images /usr/share/nginx/html/images
COPY marnost.ico /usr/share/nginx/html/marnost.ico

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
