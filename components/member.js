import Head from 'next/head'
import styles from '../styles/Home.module.css'
import Layout from './layout'
import rss_parser from '../utils/parser'
const parser = require('xml2json')
const rss = require('../rss/rss')

function Member({ member }) {
    return (
        <Layout>
            <div className={styles.grid}>
                {
                    member.map(item => (
                        <a href={item.link} className={styles.card, styles.membercard}>
                            <span className={styles.cardtitle}>{item.title}</span>
                            <div className={styles.carddetail}>
                                <a href={item.home} className={styles.cardhome}>
                                    <span className={styles.cardauthor}>{item.author}</span>
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
    let rsss = rss.default.rss
    const len = rsss.length
    let member = []
    for (let i = 0; i < len; i++) {
        let result = await fetch(rsss[i].link)
        let res = await result.text()
        let rss_json = parser.toJson(res, { object: true })
        let parse_data = rss_parser.run(rss_json, rsss[i].method, { type: 'member' })
        member.push({
            title: parse_data.title,
            author: rsss[i].author,
            link: parse_data.link,
            date: parse_data.date,
        })
    }

    return {
        props: {
            member
        },
        fallback: false
    }
}

export default Member