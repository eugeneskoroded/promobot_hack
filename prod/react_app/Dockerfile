# pull the base image
FROM node:lts-alpine

# set the working direction
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./

# rebuild node-sass
COPY . ./
RUN npm install
RUN npm run build

# add app

EXPOSE 8080
# start app
CMD ["npm", "run", "preview"]
