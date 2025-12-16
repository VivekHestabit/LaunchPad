function debounce(fn , delay){
    let timer;
    return function(...args){
        clearTimeout(timer);
        timer = setTimeout(()=>{
            fn(...args);
        } , delay)
    }
} 



// throttle fucntion : 

function throttle(fn, limit) {
let flag = true;
return function (...args) {
if (flag) {
fn(...args);
flag = false;
setTimeout(() => flag = true, limit);
}
};
}



// group by function : 


function groupBy(arr, key) {
return arr.reduce((acc, item) => {
const group = item[key];
acc[group] = acc[group] || [];
acc[group].push(item);
return acc;
}, {});
}