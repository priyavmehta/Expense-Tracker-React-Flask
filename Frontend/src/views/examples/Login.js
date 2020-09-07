/*!

=========================================================
* Argon Dashboard React - v1.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";

// reactstrap components
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  FormGroup,
  Form,
  Input,
  InputGroupAddon,
  InputGroupText,
  InputGroup,
  Row,
  Col
} from "reactstrap";
import { Link, Redirect } from "react-router-dom";
import axios from "axios";

class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loginPassword: '',
      loginUsername: '',
      loginSuccess: false,
      token: ''

    };
  }
  signInUser = async () => {
    let user = {
      username: this.state.loginUsername,

      password: this.state.loginPassword
    }


    console.log(user)
    const res = await axios.post('https://cors-anywhere.herokuapp.com/https://rpk-expense-tracker.herokuapp.com/login', user).then((response) => {
      console.log(response)
      this.setState({ ...this.state, token: `Bearer ${response.data.access_token}`, loginSuccess: true, })
    }).catch((err) => {
      console.log(err)
    })


  }
  render() {

    if (this.state.loginSuccess) {
      console.log(this.state.loginSuccess)
      return (<Redirect to={{
        pathname: '/dashboard',
        state: { access_token: this.state.token }
      }} />)
    }
    return (

      <Col lg="5" md="7">
        <Card className="bg-secondary shadow border-0">
          {/* <CardHeader className="bg-transparent pb-5">
              <div className="text-muted text-center mt-2 mb-3">
                <small>Sign in with</small>
              </div>
              <div className="btn-wrapper text-center">
                <Button
                  className="btn-neutral btn-icon"
                  color="default"
                  href="#pablo"
                  onClick={e => e.preventDefault()}
                >
                  <span className="btn-inner--icon">
                    <img
                      alt="..."
                      src={require("assets/img/icons/common/github.svg")}
                    />
                  </span>
                  <span className="btn-inner--text">Github</span>
                </Button>
                <Button
                  className="btn-neutral btn-icon"
                  color="default"
                  href="#pablo"
                  onClick={e => e.preventDefault()}
                >
                  <span className="btn-inner--icon">
                    <img
                      alt="..."
                      src={require("assets/img/icons/common/google.svg")}
                    />
                  </span>
                  <span className="btn-inner--text">Google</span>
                </Button>
              </div>
            </CardHeader> */}
          <CardBody className="px-lg-5 py-lg-5">
            <div className="text-center text-muted mb-4">
              <h4 className='lead font-weight-bold'>Sign In</h4>
            </div>
            <Form role="form">
              <FormGroup className="mb-3">
                <InputGroup className="input-group-alternative">
                  <InputGroupAddon addonType="prepend">
                    <InputGroupText>
                      <i className="ni ni-circle-08" />
                    </InputGroupText>
                  </InputGroupAddon>
                  <Input placeholder="Username" type="text" autoComplete="new-email" onChange={(e) => {
                    this.setState({ ...this.state, loginUsername: e.target.value })

                  }} />
                </InputGroup>
              </FormGroup>
              <FormGroup>
                <InputGroup className="input-group-alternative">
                  <InputGroupAddon addonType="prepend">
                    <InputGroupText>
                      <i className="ni ni-lock-circle-open" />
                    </InputGroupText>
                  </InputGroupAddon>
                  <Input placeholder="Password" type="password" autoComplete="new-password" onChange={(e) => {
                    this.setState({ ...this.state, loginPassword: e.target.value })

                  }} />
                </InputGroup>
              </FormGroup>
              {/* <div className="custom-control custom-control-alternative custom-checkbox">
                  <input
                    className="custom-control-input"
                    id=" customCheckLogin"
                    type="checkbox"
                  />
                  <label
                    className="custom-control-label"
                    htmlFor=" customCheckLogin"
                  >
                    <span className="text-muted">Remember me</span>
                  </label>
                </div> */}
              <div className="text-center">
                <Button className="my-4" color="primary" type="button" onClick={this.signInUser}>
                  Sign in
                  </Button>
              </div>
            </Form>
            <Row>

              <Col className="text-center" xs="12">

                <button
                  className="btn btn-link"
                  onClick={e => e.preventDefault()}
                >
                  <Link to='/register'><small>Create account</small></Link>
                </button>
              </Col>
            </Row>
          </CardBody>
        </Card>

      </Col>

    );
  }
}

export default Login;
