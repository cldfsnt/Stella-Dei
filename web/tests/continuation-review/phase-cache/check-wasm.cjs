const fs=require('node:fs');
(async()=>{const {instance}=await WebAssembly.instantiate(fs.readFileSync(process.argv[2]));const failures=instance.exports.parity_run(),count=instance.exports.parity_count();console.log(JSON.stringify({target:'wasm32-freestanding',failures,count}));if(failures!==0||count!==15316)process.exitCode=1;})().catch(error=>{console.error(error);process.exitCode=1});
