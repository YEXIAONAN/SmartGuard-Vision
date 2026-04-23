import dotenv from 'dotenv'
import app from './app.js'

dotenv.config()

const port = Number(process.env.PORT || 3000)

app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`SmartGuard server running at http://127.0.0.1:${port}`)
})
