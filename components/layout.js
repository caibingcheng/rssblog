import Header from './header'
import Title from './title'
import Action from './action'
import Footer from './footer'
import styles from '../styles/Home.module.css'

const Layout = props => (
    <div className={styles.container} id="top-header">
      <Header />
      <main className={styles.main}>
      <Title />
          {props.children}
      <Action />
    </main>
    <Footer />
  </div>
)

export default Layout;