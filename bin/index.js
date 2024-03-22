#! /usr/bin/env node
console.log("Hello World!");
const yargs = require("yargs");

const usage = "\n Usage: go2web <lang_name> sentence to be translated"; const options = yargs  
      .usage(usage)  
      .option("l", {alias:"languages", describe: "List all supported languages.", type: "boolean", demandOption
: false })                                                                                                    
      .help(true)  
      .argv;
      