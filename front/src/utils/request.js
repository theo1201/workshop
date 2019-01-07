import Axios from 'axios';

import Qs from 'qs'

const service = Axios.create({
    baseURL:'api',
    timeout:1000,
    headers:{'Content-Type': 'application/x-www-form-urlencoded'},
    transformRequest:[ data=>Qs.stringify(data)]
})


