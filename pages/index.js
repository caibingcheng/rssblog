import dynamic from 'next/dynamic'
import styles from '../styles/Home.module.css'
import Layout from './components/layout'
import rss_parser from './parser'
const parser = require('xml2json')
const rss = require('../rss/rss')

function Home({ data }) {
    return (
        <Layout>
            <p className={styles.updatetime}>
                Last updated at {data.meta.updatetime}
                <p>
                    update policy 0 0,6,8,10,12,14,16,18,20,22 * * * *
                </p>
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
        </Layout>
    )
}

export const getStaticProps = async () => {
    const rsss = rss.default.rss
    const len = rsss.length
    let data = []
    for (let i = 0; i < len; i++) {
        let result = await fetch(rsss[i].link)
        let res = await result.text()
        let rss_json = parser.toJson(res, { object: true })
        let parse_data = rss_parser.run(rss_json, rsss[i].method)
        parse_data.map(each => (
            each.author = rsss[i].author,
            data.push(each)
        ))
    }

    let date = new Date()
    data = {
        data: rss_parser.sort(data),
        meta: {
            updatetime: date.toUTCString()
        }
    }

    return {
        props: {
            data
        }
    }
}

export default Home