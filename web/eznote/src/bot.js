const puppeteer = require('puppeteer')
const process = require('process')
const fs = require('fs')

const FLAG = (() => {
    let flag = 'flag{test}'
    if (fs.existsSync('flag.txt')){
        flag = fs.readFileSync('flag.txt').toString()
        fs.unlinkSync('flag.txt')
    } 
    return flag
})()

const HEADLESS = !!(process.env.PROD ?? false)

const sleep = (sec) => new Promise(r => setTimeout(r, sec * 1000))

async function visit(url) {
    let browser = await puppeteer.launch({
        headless: HEADLESS,
        executablePath: '/usr/bin/chromium',
        args: ['--no-sandbox'],
    })
    let page = await browser.newPage()

    await page.goto('http://localhost:3000/')

    await page.waitForSelector('#title')
    await page.type('#title', 'flag', {delay: 100})
    await page.type('#content', FLAG, {delay: 100})
    await page.click('#submit', {delay: 100})

    await sleep(3)
    console.log('visiting %s', url)

    await page.goto(url)
    await sleep(30)
    await browser.close()
}

module.exports = {
    visit
}