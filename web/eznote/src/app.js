const express = require('express')
const session = require('express-session')
const { randomBytes } = require('crypto')
const fs = require('fs')
const spawn = require('child_process')
const path = require('path')
const { visit } = require('./bot')
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');

const DOMPurify = createDOMPurify(new JSDOM('').window);

const LISTEN_PORT = 3000
const LISTEN_HOST = '0.0.0.0'

const app = express()

app.set('views', './views')
app.set('view engine', 'html')
app.engine('html', require('ejs').renderFile)

app.use(express.urlencoded({ extended: true }))

app.use(session({
    secret: randomBytes(4).toString('hex'),
    saveUninitialized: true,
    resave: true,

}))

app.use((req, res, next) => {
    if (!req.session.notes) {
        req.session.notes = []
    }
    next()
})

const notes = new Map()

setInterval(() => { notes.clear() }, 60 * 1000);

function toHtml(source, format){
    if (format == undefined) {
        format = 'markdown'
    }
    if (!fs.existsSync("notes")) {
        fs.mkdirSync("notes");
    }
    let tmpfile = path.join('notes', randomBytes(4).toString('hex'))
    fs.writeFileSync(tmpfile, source)
    let res = spawn.execSync(`pandoc -f ${format} ${tmpfile}`).toString()
    // fs.unlinkSync(tmpfile)
    return DOMPurify.sanitize(res)
}

app.get('/ping', (req, res) => {
    res.send('pong')
})

app.get('/', (req, res) => {
    res.render('index', { notes: req.session.notes })
})

app.get('/notes', (req, res) => {
    res.send(req.session.notes)
})

app.get('/note/:noteId', (req, res) => {
    let { noteId } = req.params
    if(!notes.has(noteId)){
        res.send('no such note')
        return
    } 
    let note = notes.get(noteId)
    res.render('note', note)
})

app.post('/note', (req, res) => {
    let noteId = randomBytes(8).toString('hex')
    let { title, content, format } = req.body
    if (!/^[0-9a-zA-Z]{1,10}$/.test(format)) {
        res.send("illegal format!!!")
        return
    }
    notes.set(noteId, {
        title: title,
        content: toHtml(content, format)
    })
    req.session.notes.push(noteId)
    res.send(noteId)
})

app.get('/report', (req, res) => {
    res.render('report')
})

app.post('/report', async (req, res) => {
    let { url } = req.body
    try {
        await visit(url)
        res.send('success')
    } catch (err) {
        console.log(err)
        res.send('error')
    }
})

app.listen(LISTEN_PORT, LISTEN_HOST, () => {
    console.log(`listening on ${LISTEN_HOST}:${LISTEN_PORT}`)
})
