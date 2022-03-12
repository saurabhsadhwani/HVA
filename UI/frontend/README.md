# Installation Procedure

## NodeJS and dependencies

<br>

## Windows

Download and Install NodeJS official setup from [https://nodejs.org/en/download/](https://nodejs.org/en/download/) in local machine.


```
cd ../HVA/UI/frontend
npm install
npm run serve
```

Now Vue Application will be up and running on server [http://localhost:8080/](http://localhost:8080/).

<br>

## Linux (CentOS 8)

```

cd ../HVA/UI/frontend
curl -sL https://rpm.nodesource.com/setup_16.x | sudo bash -
sudo yum -y install nodejs
npm install
npm run serve
```