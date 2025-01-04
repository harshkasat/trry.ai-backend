'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Play, Pencil, Eye, Trash2 } from 'lucide-react'

const initialFlows = [
  { name: 'Book a home', url: 'https://airbnb.com', lastRunStatus: 'Success', lastRunTime: 'Yesterday at 11:59 PM' },
  { name: 'Publish a home', url: 'https://airbnb.com/host/homes', lastRunStatus: 'Running', lastRunTime: 'Now' },
  { name: 'Register as a host', url: 'https://airbnb.com/host/register', lastRunStatus: 'Success', lastRunTime: '9/14/2024 at 4:30 PM' },
  // Add more flows as needed
]

export default function FlowTable() {
  const [flows, setFlows] = useState(initialFlows)

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-gray-900 rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">fix ai</h2>
          <div className="space-x-2">
            <Button variant="outline" className="text-white border-white hover:bg-white hover:text-black">
              Run All
            </Button>
            <Button variant="outline" className="text-white border-white hover:bg-white hover:text-black">
              Create
            </Button>
          </div>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Flow Name</TableHead>
              <TableHead>URL</TableHead>
              <TableHead>Last Run Status</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {flows.map((flow, index) => (
              <TableRow key={index}>
                <TableCell>{flow.name}</TableCell>
                <TableCell className="text-blue-400">{flow.url}</TableCell>
                <TableCell>
                  <span className={`px-2 py-1 rounded ${
                    flow.lastRunStatus === 'Success' ? 'bg-green-800 text-green-200' :
                    flow.lastRunStatus === 'Running' ? 'bg-yellow-800 text-yellow-200' :
                    'bg-red-800 text-red-200'
                  }`}>
                    {flow.lastRunStatus}
                  </span>
                  <span className="ml-2 text-gray-400">{flow.lastRunTime}</span>
                </TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <Button size="icon" variant="ghost">
                      <Play className="h-4 w-4" />
                    </Button>
                    <Button size="icon" variant="ghost">
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button size="icon" variant="ghost">
                      <Eye className="h-4 w-4" />
                    </Button>
                    <Button size="icon" variant="ghost">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  )
}

