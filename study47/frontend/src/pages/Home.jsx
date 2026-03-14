import { useState, useEffect } from 'react'
import { api } from '@utils/network.js'

const Home = () => {
  const [list, setList] = useState([])
  const [item, setItem] = useState({ email: "", content: "" })
  const eventList = e => {
    e.preventDefault()
    api.get("/webhook-test/app")
      .then(res => {
        // console.log(res)
        setList(res.data.result)
      })
      .catch(err => {
        console.log(err)
      });
  }
  const eventSubmit = e => {
    e.preventDefault()
    api.post("/webhook-test/app", { params: item })
      .then(res => {
        // console.log(res)
        if (res.data.status) setItem({ email: "", content: "" })
        setList(res.data.result)
      })
      .catch(err => {
        console.log(err)
      });
  }
  const setChange = e => {
    setItem({ ...item, [e.target.name]: e.target.value })
  }
  useEffect(() => {

  }, [])
  return (
    <div className="container mt-3">
      <h1 className="display-1 text-center">n8n</h1>
      <form onSubmit={eventSubmit}>
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email</label>
          <input type="email" className="form-control" name="email" id="email" required placeholder="name@example.com" value={item.email} onChange={setChange} />
        </div>
        <div className="mb-3">
          <label htmlFor="content" className="form-label">Content</label>
          <textarea className="form-control" name="content" id="content" rows="3" value={item.content} onChange={setChange}></textarea>
        </div>
        <div className="btn-group w-100">
          <button type="button" className="btn btn-primary" onClick={eventList}>불러오기</button>
          <button type="submit" className="btn btn-primary">추가</button>
          <button type="button" className="btn btn-primary">삭제</button>
        </div>
      </form>
      <div className="list-group mt-3">
        {list.map((v, i) => (
          <button key={v.no} type="button" className="list-group-item list-group-item-action">{v.content}</button>
        ))
        }
      </div>
    </div>
  )
}

export default Home