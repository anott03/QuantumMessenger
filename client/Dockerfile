from node:current-alpine3.14

copy . ./app
workdir app

expose 3000

run ["npm", "i"]
entrypoint ["npm", "run", "start"]
