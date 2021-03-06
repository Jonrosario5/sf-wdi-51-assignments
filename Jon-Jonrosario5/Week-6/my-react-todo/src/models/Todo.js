import axios from 'axios';

const endpoint = `https://super-crud-api.herokuapp.com/api/todos`;

class TodoModel {
    
    
    static all(){
        let request = axios.get(endpoint)
        return(request)
    
    }

    static create(todo) {
        let request = axios.post(endpoint, todo)
        return request
      }

    static delete(todo){
        let request = axios.delete(`${endpoint}/${todo._id}`)
        return request
    }
    
}

export default TodoModel;