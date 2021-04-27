import Head from 'next/head'
import styles from '../styles/Home.module.css'
const parser = require('xml2json')
const rss = require('../rss/rss')

function Home({ data }) {
  return (
    <div className={styles.container} id="top-header">
      <Head>
        <title>RSSBlog</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          RSSBlog
        </h1>

        <p className={styles.description}>
          A Site for Blog RSS.
        </p>
        <p className={styles.updatetime}>
          Last updated at {data.meta.updatetime}
        </p>

        <div className={styles.grid}>
          {
            data.data.map(item => (
              <a href={item.link} className={styles.card}>
                <span className={styles.cardindex}>{item.index}. &nbsp;&nbsp;</span>
                <span className={styles.cardtitle}>{item.title}</span>
                <div className={styles.carddetail}>
                  <span className={styles.cardate}>{item.date}</span>
                  <a href={item.home} className={styles.cardhome}><
                    span className={styles.cardauthor}>{item.author}</span>
                  </a>
                </div>
              </a>
            ))
          }
        </div>

        <div className={styles.fixedbox}>
          <a className={styles.actiongithub} href="https://github.com/caibingcheng/rssblog" title="GitHub" target="_blank" rel="noopener noreffer me"></a>
          <a className={styles.actiontop} href="#top-header"></a>
          <a className={styles.actionbottom} href="#bottom-footer"></a>
        </div>

      </main>

      <footer className={styles.footer} id="bottom-footer">
        <a
          href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <img src="/vercel.svg" alt="Vercel Logo" className={styles.logo} />
        </a>
      </footer>
    </div>
  )
}

export const getStaticProps = async () => {
  const rsss = rss.default.rss
  const len = rsss.length
  let data = []
  for (let i = 0; i < len; i++) {
    let result = await fetch(rsss[i].link)
    let res = await result.text()
    let rss_parse = parser.toJson(res, { object: true })
    let item = rss_parse.rss.channel.item
    item.map(each => (
      each.author = rsss[i].author,
      each.home = rss_parse.rss.channel.link,
      data.push(each)
    ))
  }

  data.map(each => {
    let date = new Date(each.pubDate)
    each.timestamp = date.getTime()
    let month = date.getMonth() + 1
    month = month < 10 ? ('0' + month) : ('' + month)
    let ddate = date.getDate()
    ddate = ddate < 10 ? ('0' + ddate) : ('' + ddate)
    each.date = date.getFullYear() + '-' + month + '-' + ddate
  })
  data.sort(function (d1, d2) {
    return d2.timestamp - d1.timestamp
  })
  let i = 1;
  data.map(each => {
    each.index = i;
    i = i + 1;
  })

  let date = new Date()
  let month = date.getMonth() + 1
  month = month < 10 ? ('0' + month) : ('' + month)
  let ddate = date.getDate()
  ddate = ddate < 10 ? ('0' + ddate) : ('' + ddate)
  let hour = date.getHours()
  hour = hour < 10 ? ('0' + hour) : ('' + hour)
  let minute = date.getMinutes()
  minute = minute < 10 ? ('0' + minute) : ('' + minute)
  let second = date.getSeconds()
  second = second < 10 ? ('0' + second) : ('' + second)
  let updatetime = date.getFullYear() + '-' + month + '-' + ddate + ' ' + hour + ':' + minute + ':' + second
  data = {
    data: data,
    meta: {
      updatetime: updatetime
    }
  }

  return {
    props: {
      data
    }
  }
}

export default Home