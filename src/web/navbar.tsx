import Image from 'next/image'
import './globals.css'

export default function Navbar() {
  return (
    <main className=" text-white overflow-x-hidden relative">
        <nav className='Navbar flex items-center justify-between px-[50px] pt-[30px] text-[30px] w-[100vw] font-Merriweather '>
            <div className="logo text-[#006D77] font-black">Rotom</div>
            <ul className='RightNav flex items-center text-[#006D77] font-black'>
                <li className='mx-[35px] hover:text-[#FDFCDC] duration-300'><a href="">About Us</a></li>
                <li className='mx-[35px] hover:text-[#FDFCDC] duration-300'><a href="">Guides</a></li>
                <li className='mx-[35px] bg-[#E29578] rounded-[80px] px-[20px] py-[3px] hover:text-[#FDFCDC] hover:bg-[#006D77] duration-300 '><a href="">Get Started</a></li>
            </ul>
        </nav>
    </main>
  );
}